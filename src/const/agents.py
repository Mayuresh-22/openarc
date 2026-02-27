import os

from src.config.config import ROOT_PATH
from types.agents import AllAgentMemoryPaths


MEMORY_BASE_PATH = os.path.join(ROOT_PATH, "src/memory")
ALL_AGENT_MEMORY = {
    "PLANNER_AGENT": "planner_memory.db",
    "EXECUTOR_AGENT": "executor_memory.db",
    "VERIFIER_AGENT": "verifier_memory.db",
}


agent_memory_paths = {}
for key, path in ALL_AGENT_MEMORY.items():
    full_path = os.path.join(MEMORY_BASE_PATH, path)
    agent_memory_paths[key] = full_path


ALL_AGENT_MEMORY_PATHS: AllAgentMemoryPaths = AllAgentMemoryPaths(**agent_memory_paths)