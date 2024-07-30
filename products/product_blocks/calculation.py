# type: ignore
from uuid import UUID
from pathlib import Path

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle


class CalculationBlockInactive(
    ProductBlockModel,
    product_block_name="Calculation Metadata",
    lifecycle=[SubscriptionLifecycle.INITIAL, SubscriptionLifecycle.PROVISIONING],
):
    engine: str | None = None
    calculation_id: UUID | None = None
    script_path: Path | None = None


class CalculationBlock(
    CalculationBlockInactive, lifecycle=[SubscriptionLifecycle.ACTIVE]
):
    engine: str
    calculation_id: UUID
    script_path: Path
