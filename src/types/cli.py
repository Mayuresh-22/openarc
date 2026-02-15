from typing import Optional

from pydantic import BaseModel


class CLIOutput(BaseModel):
    stdout: Optional[str]
    stderr: Optional[str]
    exitcode: int

class CLIIntermediateInput(BaseModel):
    input_type: str
    content: list[str] = []
