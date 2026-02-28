from enum import Enum
import os
from src.config.config import ROOT_PATH
from src.types.agents import AllAgentMemoryPaths


# SUPPORTED_AGENTS enum to avoid hardcoding agent names across the codebase and reduce risk of typos
class SUPPORTED_AGENTS(Enum):
    PLANNER_AGENT = "planner"
    EXECUTOR_AGENT = "executor"
    VERIFIER_AGENT = "verifier"


MEMORY_BASE_PATH = os.path.join(ROOT_PATH, "src/memory")
ALL_AGENT_MEMORY = {
    SUPPORTED_AGENTS.PLANNER_AGENT.name: "planner_memory.db",
    SUPPORTED_AGENTS.EXECUTOR_AGENT.name: "executor_memory.db",
    SUPPORTED_AGENTS.VERIFIER_AGENT.name: "verifier_memory.db",
}

agent_memory_paths = {}
for key, path in ALL_AGENT_MEMORY.items():
    full_path = os.path.join(MEMORY_BASE_PATH, path)
    agent_memory_paths[key] = full_path

ALL_AGENT_MEMORY_PATHS: AllAgentMemoryPaths = AllAgentMemoryPaths(**agent_memory_paths)
