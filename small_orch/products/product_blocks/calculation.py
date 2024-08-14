# type: ignore
from uuid import UUID
from pathlib import Path

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle
from pydantic import field_serializer


class CalculationBlockInactive(
    ProductBlockModel,
    product_block_name="Calculation Metadata",
    lifecycle=[SubscriptionLifecycle.INITIAL, SubscriptionLifecycle.PROVISIONING],
):
    engine: str | None = None
    calculation_id: UUID | None = None
    script_path: str | None = None

    @field_serializer("script_path", when_used="json-unless-none")
    def serialize_script_path(script_path: Path) -> str:
        return str(script_path)


class CalculationBlock(
    CalculationBlockInactive, lifecycle=[SubscriptionLifecycle.ACTIVE]
):
    engine: str
    calculation_id: UUID
    script_path: str
