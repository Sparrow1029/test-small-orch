from orchestrator.workflows import LazyWorkflowInstance

# Calculation
LazyWorkflowInstance(
    "small_orch.workflows.calculation.create_calculation", "create_calculation"
)
LazyWorkflowInstance(
    "small_orch.workflows.calculation.run_calculation", "run_calculation"
)
