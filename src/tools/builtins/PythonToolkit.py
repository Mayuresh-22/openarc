from agno.tools.python import PythonTools

from src.config.config import CWD_PATH
from src.tools.registry import ToolRegistry


class PythonToolkit(PythonTools):
    def __init__(self):
        super().__init__(base_dir=CWD_PATH)


ToolRegistry().register_toolkit(PythonToolkit())
