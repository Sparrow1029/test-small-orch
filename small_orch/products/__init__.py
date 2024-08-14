from orchestrator.domain import SUBSCRIPTION_MODEL_REGISTRY

from .product_types.calculation import Calculation

SUBSCRIPTION_MODEL_REGISTRY.update({"Calculation": Calculation})
