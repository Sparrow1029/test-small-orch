# type: ignore
from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle
from ..product_blocks.calculation import CalculationBlockInactive, CalculationBlock


class CalculationInactive(SubscriptionModel, is_base=True):
    calculation: CalculationBlockInactive


class CalculationProvisioning(
    CalculationInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    calculation: CalculationBlockInactive


class Calculation(CalculationProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    calculation: CalculationBlock
