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
    plan: list[PlanStep]
