from typing import Callable

from src.const.agents import SUPPORTED_AGENTS
from src.core.agents.agent_config_service import AgentConfigService
from src.core.prompts.prompt import PromptService
from src.const.config import ConfigMenuOptionsValue
from src.llm.llm_provider_registry import LLMProviderRegistry
from src.core.ui.config_menu_ui import ConfigMenuUI
from src.core.handlers.base_handler import BaseHandler
from src.types.cli import CLIOutput
from src.types.config import AvailableLLMProvider


class ArcCommandHandler(BaseHandler):
    _instance = None

    def __new__(cls, *args, **kwargs) -> "ArcCommandHandler":
        if cls._instance is None:
            cls._instance = super(ArcCommandHandler, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        config_menu_ui_handler: ConfigMenuUI,
        llm_provider_registry: LLMProviderRegistry,
        agent_config_service: AgentConfigService,
        prompt_service: PromptService,
    ):
        super().__init__()
        self.valid_arc_commands_map: dict[str, Callable] = {
            "config": self.config_command,
            "help": self.help_command,
            "bye": self.bye_command,
        }
        self.config_menu_ui_handler = config_menu_ui_handler
        self.llm_provider_registry = llm_provider_registry
        self.agent_config_service = agent_config_service
        self.prompt_service = prompt_service

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
            case ConfigMenuOptionsValue.OPTION_ADD_PROVIDER.value:
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
                self.llm_provider_registry.register_llm_provider(new_provider)

                # If this is the first provider being added, set it as the model for all agents by default
                if len(self.llm_provider_registry.get_available_llm_providers()) == 1:
                    for agents in SUPPORTED_AGENTS:
                        self.agent_config_service.set_agent_model(
                            agent_name=agents.value, llm_provider=new_provider
                        )

                return CLIOutput(
                    stdout=f"Added LLM provider: {llm_provider.name} with model ID {model_id}",  # type: ignore
                    stderr=None,
                    exitcode=0,
                )

            case ConfigMenuOptionsValue.OPTION_SWITCH_PROVIDER.value:
                llm_provider = self.config_menu_ui_handler.handle_switch_llm_provider(
                    self.llm_provider_registry.get_available_llm_providers()
                )
                selected_agents = self.config_menu_ui_handler.select_agents_for_switch()

                if llm_provider is None:
                    return CLIOutput(
                        stdout="LLM provider switching cancelled.",
                        stderr=None,
                        exitcode=0,
                    )

                for agent in selected_agents:
                    self.agent_config_service.set_agent_model(agent, llm_provider)  # type: ignore

                return CLIOutput(
                    stdout=f"LLM/provider switch completed.",
                    stderr=None,
                    exitcode=0,
                )

            case ConfigMenuOptionsValue.OPTION_MOD_SYS_PROMPT.value:
                new_sys_prompt = self.config_menu_ui_handler.handle_mod_sys_prompt(
                    current_sys_prompt=self.prompt_service.get_sys_prompt()
                )
                self.prompt_service.set_sys_prompt(new_sys_prompt)

                return CLIOutput(
                    stdout="System prompt updated successfully.",
                    stderr=None,
                    exitcode=0,
                )

            case ConfigMenuOptionsValue.OPTION_MOD_USER_PROMPT.value:
                new_user_prompt = self.config_menu_ui_handler.handle_mod_user_prompt(
                    current_user_prompt=self.prompt_service.get_user_prompt()
                )
                self.prompt_service.set_user_prompt(new_user_prompt)

                return CLIOutput(
                    stdout="User prompt updated successfully.",
                    stderr=None,
                    exitcode=0,
                )

            case ConfigMenuOptionsValue.OPTION_MOD_TOOL_PROMPT.value:
                new_tool_prompt = self.config_menu_ui_handler.handle_mod_tool_prompt(
                    current_tool_prompt=self.prompt_service.get_tool_prompt()
                )
                self.prompt_service.set_tool_prompt(new_tool_prompt)

                return CLIOutput(
                    stdout="Tool prompt updated successfully.",
                    stderr=None,
                    exitcode=0,
                )

            case ConfigMenuOptionsValue.OPTION_CANCEL.value:
                return CLIOutput(
                    stdout="Returning to Main Menu.", stderr=None, exitcode=0
                )

        return CLIOutput(stdout=result, stderr=None, exitcode=0)

    def bye_command(self):
        print("Exiting OpenArc. Goodbye!")
        exit(0)

    def help_command(self) -> CLIOutput:
        help_text = (
            "Available commands:\n"
            "  /config - Configure the system settings.\n"
            "  /help - Show this help message.\n"
            "  /bye - Exit the OpenArc."
        )
        return CLIOutput(stdout=help_text, stderr=None, exitcode=0)
