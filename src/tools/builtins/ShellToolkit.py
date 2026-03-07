from agno.tools.shell import ShellTools

from src.config.config import CWD_PATH
from src.tools.registry import ToolRegistry


class ShellToolkit(ShellTools):
    def __init__(self):
        super().__init__(
            base_dir=CWD_PATH
        )


ToolRegistry().register_toolkit(ShellToolkit())
