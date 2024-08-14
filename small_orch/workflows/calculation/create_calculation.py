from pathlib import Path
from typing import TypeAlias, cast

from orchestrator import step, begin
from orchestrator.types import State, SubscriptionLifecycle, UUIDstr
from orchestrator.settings import app_settings
from orchestrator.workflow import StepList
from orchestrator.workflows.utils import create_workflow
from orchestrator.workflows.steps import set_status
from pydantic import ConfigDict
from pydantic_forms.types import FormGenerator
from pydantic_forms.validators import Choice
from pydantic_forms.core import FormPage
from structlog import get_logger

from small_orch.products.product_types.calculation import CalculationInactive

logger = get_logger(__name__)

# This would likely be a pathlib.Path.iterdir() from somewhere on the server where the scripts are stored
# or similar dynamic fetching
SCRIPTS = [
    "/usr/local/bin/scripts/my_script.sh",
    "/usr/local/bin/scripts/other_script.sh",
]


class EngineEnum(Choice):
    pytorch = "pytorch"
    tensorflow = "tensorflow"


def initial_input_form_generator(workflow_name: str) -> FormGenerator:
    ScriptChoice: TypeAlias = cast(type[Choice], Choice("ScriptEnum", zip(SCRIPTS, SCRIPTS)))  # type: ignore

    class CreateCalculationForm(FormPage):
        model_config = ConfigDict(title=" ".join(workflow_name.split("_")).title())

        script_choice: ScriptChoice
        engine_choice: EngineEnum = EngineEnum.pytorch
        calculation_name: str

    logger.info("## SCHEMA: ", schema=CreateCalculationForm.model_json_schema())

    user_input = yield CreateCalculationForm

    return user_input.model_dump()


@step("Construct subscription model")
def construct_model(
    product: UUIDstr,
    script_choice: Path,
    engine_choice: str,
    calculation_name: str,
) -> State:
    subscription = CalculationInactive.from_product_id(
        product, customer_id=app_settings.DEFAULT_CUSTOMER_IDENTIFIER
    )
    subscription.description = calculation_name

    subscription.calculation.script_path = str(script_choice)
    subscription.calculation.engine = engine_choice
    subscription.calculation.calculation_id = (
        subscription.calculation.subscription_instance_id
    )

    return {"subscription": subscription}


@create_workflow(
    "Create Calculation Subscription",
    initial_input_form=initial_input_form_generator,
)
def create_calculation() -> StepList:
    return begin >> construct_model >> set_status(SubscriptionLifecycle.ACTIVE)
