from agno.tools.calculator import CalculatorTools

from src.tools.registry import ToolRegistry


class CalculatorToolkit(CalculatorTools):
    def __init__(self):
        super().__init__()


ToolRegistry().register_toolkit(CalculatorToolkit())
