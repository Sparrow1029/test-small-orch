import subprocess
from orchestrator.types import State, UUIDstr
from orchestrator.workflow import StepList, begin, step

from orchestrator.workflows.utils import (
    modify_workflow,
)
from structlog import get_logger

from small_orch.products.product_types.calculation import Calculation

logger = get_logger(__name__)


@step("Load initial state")
def load_initial_state_for_modify(subscription_id: UUIDstr) -> State:
    subscription = Calculation.from_subscription(subscription_id)
    return {"subscription": subscription}


@step("Run calculation")
def execute_calcuation(subscription: Calculation) -> State:
    logger.info(
        f"Running calculation with command '{subscription.calculation.engine} {subscription.calculation.script_path}'"
    )
    result = subprocess.run(
        [subscription.calculation.engine, subscription.calculation.script_path],
        check=True,
        capture_output=True,
    )
    result.check_returncode()
    logger.info("Result", stdout=result.stdout, stderr=result.stderr)
    return {
        "calculation_output": result.stdout.decode("utf-8"),
        "calculation_stderr": result.stderr.decode("utf-8"),
    }


@modify_workflow("Run the calculation")
def run_calculation() -> StepList:
    return begin >> load_initial_state_for_modify >> execute_calcuation
