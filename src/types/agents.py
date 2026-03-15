from pydantic import BaseModel


class AllAgentMemoryPaths(BaseModel):
    PLANNER_AGENT: str
    EXECUTOR_AGENT: str
    VERIFIER_AGENT: str


class PlanStep(BaseModel):
    step_name: str
    step_description: str
    tools_required: list[str]
    expected_output: str


class PlannerAgentOutputSchema(BaseModel):
    task: str
    plan: list[PlanStep]


class ExecutorAgentOutputSchema(BaseModel):
    execution_results: list[str]
