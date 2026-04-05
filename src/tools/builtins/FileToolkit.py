from agno.tools.file import FileTools

from src.config.config import CWD_PATH
from src.tools.registry import ToolRegistry


class FileToolkit(FileTools):
    def __init__(self):
        super().__init__(base_dir=CWD_PATH)


ToolRegistry().register_toolkit(FileToolkit())
