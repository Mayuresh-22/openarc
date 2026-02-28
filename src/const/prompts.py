import os

from src.config.config import ROOT_PATH
from src.types.prompts import AllPromptsFilePath
from src.utils.file import ensure_file_exists


BASE_PROMPT_FILE_PATH = os.path.join(ROOT_PATH, "src/core/prompts/prompt_files")
ALL_PROMPT_FILES = {
    "SYSTEM_PROMPT_FILE_PATH": "SYSTEM_PROMPT.md",
    "USER_PROMPT_FILE_PATH": "USER_PROMPT.md",
    "TOOL_PROMPT_FILE_PATH": "TOOL_PROMPT.md",
}

prompt_paths = {}
for key, path in ALL_PROMPT_FILES.items():
    full_path = os.path.join(BASE_PROMPT_FILE_PATH, path)
    ensure_file_exists(full_path)
    prompt_paths[key] = full_path


ALL_PROMPTS_FILE_PATH: AllPromptsFilePath = AllPromptsFilePath(**prompt_paths)
