from pydantic import BaseModel


class AllAgentMemoryPaths(BaseModel):
    PLANNER_AGENT: str
    EXECUTOR_AGENT: str
    VERIFIER_AGENT: str
