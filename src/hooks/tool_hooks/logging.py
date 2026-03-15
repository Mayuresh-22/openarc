from typing import Callable
from prompt_toolkit import HTML, print_formatted_text

from src.utils.print_style import cli_style


def logging_hook(function_name: str, func: Callable, args: dict):
    """Log the tool name and arguments before execution."""
    print_formatted_text(
        HTML(f"\n\n<system>Calling {function_name} with args: {list(args.keys())}</system>"),
        style=cli_style
    )
    return func(**args)