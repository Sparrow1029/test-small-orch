"""This module contains functions and classes necessary for celery worker processes.

When the orchestrator-core's thread process executor is specified as "celery", the `OrchestratorCore` FastAPI
application registers celery-specific task functions and `start_process` and `resume_process` now defer to the
celery task queue.

Celery's task queue enables features like nightly validations by providing a task queue and workers to execute
workflows that are all started in parallel, which would crash a single-threaded orchestrator-core.

The application flow looks like this when "celery" is the executor (and websockets are enabled):

- FastAPI application validates form input, and places a task on celery queue (create new process).
  - If websockets are enabled, a connection should exist already b/t the client and backend.
- FastAPI application begins watching redis pubsub channel for process updates from celery.
- Celery worker picks up task from queue and begins executing.
- On each step completion, it publishes state information to redis pubsub channel.
- FastAPI application grabs this information and publishes it to the client websocket connection.

A celery worker container will start by calling this module instead of `main.py` like so:
```sh
celery -A esnetorch.celery_worker worker -E -l INFO -Q new_tasks,resume_tasks,new_workflows,resume_workflows
```

* `-A` points to this module where the worker class is defined
* `-E` sends task-related events (capturable and monitorable)
* `-l` is the short flag for --loglevel
* `-Q` specifies the queues which the worker should watch for new tasks

See https://workfloworchestrator.org/orchestrator-core/reference-docs/app/scaling for more information.
"""

from uuid import UUID

from celery import Celery
from celery.signals import worker_shutting_down  # , setup_logging
from orchestrator.db import init_database
from orchestrator.domain import SUBSCRIPTION_MODEL_REGISTRY
from orchestrator.services.tasks import initialise_celery
from orchestrator.types import BroadcastFunc
from orchestrator.websocket import (
    broadcast_process_update_to_websocket,
    init_websocket_manager,
)
from orchestrator.websocket.websocket_manager import WebSocketManager
from orchestrator.workflows import ALL_WORKFLOWS
from structlog import get_logger

from orchestrator import app_settings

# from nwastdlib.logging import initialise_logging


logger = get_logger(__name__)


# @setup_logging.connect  # type: ignore[misc]
# def on_setup_logging(**kwargs: Any) -> None:
#     initialise_logging(additional_loggers=LOGGER_OVERRIDES_CELERY)


def process_broadcast_fn(process_id: UUID) -> None:
    # Catch all exceptions as broadcasting failure is noncritical to workflow completion
    try:
        broadcast_process_update_to_websocket(process_id)
    except Exception as e:
        logger.exception(e)


class OrchestratorWorker(Celery):
    websocket_manager: WebSocketManager
    process_broadcast_fn: BroadcastFunc

    def on_init(self) -> None:
        init_database(app_settings)

        # Prepare the wrapped_websocket_manager
        # Note: cannot prepare the redis connections here as broadcasting is async
        self.websocket_manager = init_websocket_manager(app_settings)
        self.process_broadcast_fn = process_broadcast_fn

        # Load the products and load the workflows
        import small_orch.products  # noqa: F401  Side-effects
        import small_orch.workflows  # noqa: F401  Side-effects

        logger.info(
            "Loaded the workflows and products",
            workflows=len(ALL_WORKFLOWS.values()),
            products=len(SUBSCRIPTION_MODEL_REGISTRY.values()),
        )

    def close(self) -> None:
        super().close()


celery = OrchestratorWorker(
    f"{app_settings.SERVICE_NAME}-worker",
    broker=str(app_settings.CACHE_URI),
    include=["orchestrator.services.tasks"],
)

if app_settings.TESTING:
    celery.conf.update(backend=str(app_settings.CACHE_URI), task_ignore_result=False)
else:
    celery.conf.update(task_ignore_result=True)

celery.conf.update(
    result_expires=3600,
    worker_prefetch_multiplier=1,
    worker_send_task_event=True,
    task_send_sent_event=True,
)

# Needed if we load this as a Celery worker because in that case there is no 'main app'
initialise_celery(celery)


@worker_shutting_down.connect  # type: ignore
def worker_shutting_down_handler(sig, how, exitcode, **kwargs) -> None:
    logger.info(
        "Shutting down worker", sig=sig, how=how, exitcode=exitcode, extra=kwargs
    )
    celery.close()
