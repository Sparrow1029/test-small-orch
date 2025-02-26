from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle
from ..product_blocks.port import PortBlockInactive, PortBlock


class PortInactive(SubscriptionModel, is_base=True):
    port: PortBlockInactive


class PortProvisioning(PortInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    port: PortBlockInactive


class Port(PortProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    port: PortBlock
