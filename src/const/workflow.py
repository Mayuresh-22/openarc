import os

from src.config.config import ROOT_PATH


MEMORY_BASE_PATH = os.path.join(ROOT_PATH, "src/memory")
WORKFLOW_MEMORY_PATH = os.path.join(MEMORY_BASE_PATH, "workflow_memory.db")
