from pathlib import Path
from typing import NewType

import strawberry
from celery import Celery
from oauth2_lib.settings import oauth2lib_settings
from orchestrator import OrchestratorCore
from orchestrator.cli.main import app as core_cli
from orchestrator.graphql import SCALAR_OVERRIDES
from orchestrator.services.tasks import initialise_celery
from structlog import get_logger

from small_orch.settings import app_settings

logger = get_logger(__name__)

PathType = strawberry.scalar(
    NewType("PathType", Path),
    description="Allow representing a system path type",
    serialize=lambda v: str(v),
    parse_value=lambda v: Path(v),
)

UPDATED_SCALAR_OVERRIDES = SCALAR_OVERRIDES | {Path: PathType}


def init_app():
    from small_orch import (
        products,  # noqa: F401
        workflows,  # noqa: F401
    )


app = OrchestratorCore(base_settings=app_settings)
init_app()

app.register_graphql(scalar_overrides=UPDATED_SCALAR_OVERRIDES)  # type: ignore

logger.debug(
    "Settings: ",
    app=app_settings.model_dump_json(indent=2),
    oauth=oauth2lib_settings.model_dump_json(indent=2),
)


class OrchestratorCelery(Celery):
    pass


if app_settings.EXECUTOR == "celery":
    broker = str(app_settings.CACHE_URI)
    backend = str(app_settings.CACHE_URI)
    logger.info("Init celery", broker=broker, backend=backend)
    celery = OrchestratorCelery(
        __name__,
        broker=str(broker),
        backend=backend,
        include=["orchestrator.services.tasks"],
    )
    celery.conf.update(result_expires=3600)
    initialise_celery(celery)

if __name__ == "__main__":
    core_cli()
