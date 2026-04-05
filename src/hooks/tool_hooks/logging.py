
from typing import Callable
from src.utils.print_style import print_with_frame, CLI_COLORS


def logging_hook(function_name: str, func: Callable, args: dict):
    """Log the tool name and arguments before execution."""
    print_with_frame(
        f"Calling {function_name} with args: {list(args.keys())}",
        color=CLI_COLORS["system"],
        style="system"
    )
    return func(**args)
