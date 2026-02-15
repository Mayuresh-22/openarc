from src.core.handler.base_handler import BaseHandler
from src.core.handler.arc_command_handler import ArcCommandHandler
from src.core.handler.arc_query_handler import ArcQueryHandler
from src.core.handler.shell_command_handler import ShellCommandHandler


HANDLER_MAP: dict[str, type[BaseHandler]] = {
    "shell": ShellCommandHandler,
    "arc_command": ArcCommandHandler,
    "arc_query": ArcQueryHandler
}


def get_input_handler(input_type: str) -> BaseHandler:
    if input_type in HANDLER_MAP:
        return HANDLER_MAP[input_type]()
    raise ValueError(f"Unknown input type: {input_type}")
