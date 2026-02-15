import subprocess
from typing import Optional

from pydantic import BaseModel
from src.core.handler.base_handler import BaseHandler
from src.types.cli import CLIOutput


class ShellCommandHandler(BaseHandler):
    def handle(self, content) -> CLIOutput:
        try:
            result = subprocess.run(
                content, shell=True, capture_output=True, text=True, timeout=10
            )
            return CLIOutput(
                stdout=result.stdout, stderr=result.stderr, exitcode=result.returncode
            )
        except Exception as e:
            return CLIOutput(
                stdout=None, stderr=f"Error executing shell command: {e}", exitcode=1
            )
