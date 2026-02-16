from typing import Callable

from prompt_toolkit import HTML, choice, prompt
from prompt_toolkit.filters import is_done
from src.core.ui.config_menu_ui import ConfigMenuUI
from src.config.llm import SUPPORTED_MODEL_PROVIDERS
from src.core.handlers.base_handler import BaseHandler
from src.types.cli import CLIOutput


class ArcCommandHandler(BaseHandler):
    def __init__(self, config_menu_ui_handler: ConfigMenuUI):
        super().__init__()
        self.valid_arc_commands_map: dict[str, Callable] = {
            "config": self.handle_config,
            "help": self.handle_help,
        }
        self.config_menu_ui_handler = config_menu_ui_handler

    def handle(self, content: list[str]) -> CLIOutput:
        if content[0] not in self.valid_arc_commands_map:
            return CLIOutput(
                stdout=f"Unknown command: {content[0]}. Type '/help' for available commands.",
                stderr=None,
                exitcode=1,
            )
        return self.valid_arc_commands_map[content[0]]()

    def handle_config(self) -> CLIOutput:
        result = self.config_menu_ui_handler.display_config_menu()
        print()
        match result:
            case "1":
                model_choice, api_key, model_id = (
                    self.config_menu_ui_handler.handle_add_llm_provider()
                )
                return CLIOutput(
                    stdout=f"Add LLM Provider selected. (This is a placeholder action.)\nModel Choice: {model_choice}\nAPI Key: {api_key}\nModel ID: {model_id}",
                    stderr=None,
                    exitcode=0,
                )
            case "2":
                return CLIOutput(
                    stdout="Switch LLM Provider selected. (This is a placeholder action.)",
                    stderr=None,
                    exitcode=0,
                )
            case "3":
                return CLIOutput(
                    stdout="Returning to Main Menu.", stderr=None, exitcode=0
                )

        return CLIOutput(stdout=result, stderr=None, exitcode=0)

    def handle_help(self) -> CLIOutput:
        help_text = (
            "Available commands:\n"
            "  config - Configure the system settings.\n"
            "  help - Show this help message."
        )
        return CLIOutput(stdout=help_text, stderr=None, exitcode=0)
