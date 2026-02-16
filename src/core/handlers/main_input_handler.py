from src.core.handlers.arc_command_handler import ArcCommandHandler
from src.core.handlers.arc_query_handler import ArcQueryHandler
from src.core.handlers.shell_command_handler import ShellCommandHandler
from src.types.cli import CLIOutput


class MainInputHandler:
    def __init__(
        self,
        shell_command_handler: ShellCommandHandler,
        arc_command_handler: ArcCommandHandler,
        arc_query_handler: ArcQueryHandler,
    ) -> None:
        self.shell_command_handler = shell_command_handler
        self.arc_command_handler = arc_command_handler
        self.arc_query_handler = arc_query_handler

    def handle(self, input_type: str, content: list[str]) -> CLIOutput:
        match input_type:
            case "shell":
                return self.shell_command_handler.handle(content)
            case "arc_command":
                return self.arc_command_handler.handle(content)
            case "arc_query":
                return self.arc_query_handler.handle(content)
            case _:
                raise ValueError(f"Unknown input type: {input_type}")
