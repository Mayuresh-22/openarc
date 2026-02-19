from pydantic import BaseModel


class AllPromptsFilePath(BaseModel):
    SYSTEM_PROMPT_FILE_PATH: str
    USER_PROMPT_FILE_PATH: str
    TOOL_PROMPT_FILE_PATH: str
