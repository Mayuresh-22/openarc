from agno.tools.user_control_flow import UserControlFlowTools

from src.tools.registry import ToolRegistry


class UserControlFlowToolkit(UserControlFlowTools):
    def __init__(self):
        super().__init__()


ToolRegistry().register_toolkit(UserControlFlowToolkit())
