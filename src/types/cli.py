from typing import Any, Optional

from pydantic import BaseModel


class CLIOutput(BaseModel):
    stdout: Any
    stderr: Optional[str]
    exitcode: int


class CLIIntermediateInput(BaseModel):
    input_type: str
    content: list[str] = []
