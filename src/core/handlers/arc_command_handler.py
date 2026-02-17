from typing import Callable

from prompt_toolkit import HTML, choice, prompt
from prompt_toolkit.filters import is_done
from src.llm.llm_provider_registry import LLMProviderRegistry
from src.config.config import ConfigService
from src.core.ui.config_menu_ui import ConfigMenuUI
from src.config.llm import SUPPORTED_MODEL_PROVIDERS
from src.core.handlers.base_handler import BaseHandler
from src.types.cli import CLIOutput
from src.types.config import AvailableLLMProvider, CurrentLLMProvider


class ArcCommandHandler(BaseHandler):
    def __init__(
        self,
        config_menu_ui_handler: ConfigMenuUI,
        llm_provider_registry: LLMProviderRegistry,
    ):
        super().__init__()
        self.valid_arc_commands_map: dict[str, Callable] = {
            "config": self.config_command,
            "help": self.help_command,
        }
        self.config_menu_ui_handler = config_menu_ui_handler
        self.llm_provider_registry = llm_provider_registry

    def handle(self, content: list[str]) -> CLIOutput:
        if content[0] not in self.valid_arc_commands_map:
            return CLIOutput(
                stdout=f"Unknown command: {content[0]}. Type '/help' for available commands.",
                stderr=None,
                exitcode=1,
            )
        return self.valid_arc_commands_map[content[0]]()

    def config_command(self) -> CLIOutput:
        result = self.config_menu_ui_handler.display_config_menu()
        print()

        match result:
            case "1":
                llm_provider, api_key, model_id = (
                    self.config_menu_ui_handler.handle_add_llm_provider()
                )

                if not llm_provider and not api_key and not model_id:
                    return CLIOutput(
                        stdout="LLM provider addition cancelled.",
                        stderr=None,
                        exitcode=0,
                    )

                if self.llm_provider_registry.is_provider_registered(
                    llm_provider.code_name,  # type: ignore
                    model_id,  # type: ignore
                ):
                    return CLIOutput(
                        stdout=f"LLM provider {llm_provider.name} with model ID {model_id} is already registered.",  # type: ignore
                        stderr=None,
                        exitcode=0,
                    )

                new_provider = AvailableLLMProvider(
                    provider_name=llm_provider.name,  # type: ignore
                    code_name=llm_provider.code_name,  # type: ignore
                    model_id=model_id,  # type: ignore
                    api_key=api_key,  # type: ignore
                )
                self.llm_provider_registry.register_provider(new_provider)

                return CLIOutput(
                    stdout=f"Added LLM provider: {llm_provider.name} with model ID {model_id}",  # type: ignore
                    stderr=None,
                    exitcode=0,
                )

            case "2":
                llm_provider = self.config_menu_ui_handler.handle_switch_llm_provider(
                    self.llm_provider_registry.get_available_llm_providers()
                )

                if llm_provider is None:
                    return CLIOutput(
                        stdout="LLM provider switching cancelled.",
                        stderr=None,
                        exitcode=0,
                    )

                self.llm_provider_registry.set_current_provider(llm_provider)

                return CLIOutput(
                    stdout=f"Switched LLM Provider to: {llm_provider.provider_name} ({llm_provider.model_id})",  # type: ignore
                    stderr=None,
                    exitcode=0,
                )
            case "3":
                return CLIOutput(
                    stdout="Returning to Main Menu.", stderr=None, exitcode=0
                )

        return CLIOutput(stdout=result, stderr=None, exitcode=0)

    def help_command(self) -> CLIOutput:
        help_text = (
            "Available commands:\n"
            "  config - Configure the system settings.\n"
            "  help - Show this help message."
        )
        return CLIOutput(stdout=help_text, stderr=None, exitcode=0)
