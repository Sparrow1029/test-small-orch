from uuid import UUID
from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle
from pydantic import Field


class PortConfigBlockInactive(
    ProductBlockModel,
    product_block_name="Port Configuration",
    lifecycle=[SubscriptionLifecycle.INITIAL, SubscriptionLifecycle.PROVISIONING],
):
    iface_id: UUID | None = None
    device_id: int | None = None
    speed: int | None = None


class PortConfigBlock(
    PortConfigBlockInactive,
    lifecycle=[SubscriptionLifecycle.ACTIVE],
):
    iface_id: UUID
    device_id: int
    speed: int


class PortBlockInactive(
    ProductBlockModel,
    product_block_name="Port Block",
    lifecycle=[SubscriptionLifecycle.INITIAL, SubscriptionLifecycle.PROVISIONING],
):
    port_config: PortConfigBlockInactive
    lag_members: list[PortConfigBlockInactive] = []


class PortBlock(PortBlockInactive, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    port_config: PortConfigBlock
    lag_members: list[PortConfigBlock] = []
