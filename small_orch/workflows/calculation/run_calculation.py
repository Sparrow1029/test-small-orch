from orchestrator.targets import Target
from orchestrator.types import State
from orchestrator.workflow import StepList, init, done, workflow, step

# from orchestrator.workflows.utils import modify_workflow
from structlog import get_logger

from small_orch.products.product_types.calculation import Calculation

logger = get_logger(__name__)


@step("Run calculation")
def execute_calcuation(state: State):
    logger.info("State: ", state=state)


@workflow(
    "Run a calculation",
    # initial_input_form=initial_input_form_generator,
    target=Target.SYSTEM,
)
def run_calculation() -> StepList:
    return init >> execute_calcuation >> done
