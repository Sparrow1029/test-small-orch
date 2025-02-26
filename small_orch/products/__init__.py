from orchestrator.domain import SUBSCRIPTION_MODEL_REGISTRY

from .product_types.calculation import Calculation
from .product_types.port import Port

SUBSCRIPTION_MODEL_REGISTRY.update({"Calculation": Calculation, "Port": Port})
