from typing import Optional
from prompt_toolkit import HTML, choice, print_formatted_text, prompt
from prompt_toolkit.filters import is_done
from prompt_toolkit.shortcuts import checkboxlist_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Checkbox, CheckboxList
from src.const.agents import SUPPORTED_AGENTS
from src.core.prompts.prompt import PromptService
from src.const.config import CONFIG_MENU_VAL_LABEL_MAP
from src.const.llm import SUPPORTED_MODEL_PROVIDERS
from src.types.config import AvailableLLMProvider, SupportedLLMProvider
from src.utils.prompt import prompt_session


class ConfigMenuUI:
    _instance = None

    def __new__(cls, *args, **kwargs) -> "ConfigMenuUI":
        if cls._instance is None:
            cls._instance = super(ConfigMenuUI, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.supported_llm_providers: list[tuple[int, str]] = [
            (i, model.name) for i, model in enumerate(SUPPORTED_MODEL_PROVIDERS)
        ]

    def display_config_menu(self):
        menu_choice = choice(
            message="Select a configuration option:",
            options=[(key, value) for key, value in CONFIG_MENU_VAL_LABEL_MAP.items()],
            show_frame=~is_done,  # type: ignore
            bottom_toolbar=HTML(
                " Press <b>[Up]</b>/<b>[Down]</b> to select, <b>[Enter]</b> to accept."
            ),
        )
        return menu_choice

    def handle_add_llm_provider(
        self,
    ) -> tuple[Optional[SupportedLLMProvider], Optional[str], Optional[str]]:
        option_choice = choice(
            message="Enter LLM provider details:",
            options=self.supported_llm_providers + [("x", "Cancel")],
            show_frame=~is_done,  # type: ignore
        )
        print()

        if option_choice == "x":
            return None, None, None

        api_key = prompt(
            HTML("Enter API key for the selected provider: "),
            placeholder="sk-aQasd...",
            is_password=True,
            accept_default=False,
        )

        model_id = prompt(
            HTML("Enter model ID to use (e.g. gpt-4): "),
            placeholder="gpt-4",
            accept_default=False,
        )
        return SUPPORTED_MODEL_PROVIDERS[option_choice], api_key, model_id

    def handle_switch_llm_provider(
        self, available_providers: list[AvailableLLMProvider]
    ) -> Optional[AvailableLLMProvider]:
        available_model_options = [
            (i, f"{provider.provider_name} ({provider.model_id})")
            for i, provider in enumerate(available_providers)
        ]

        if not available_model_options:
            print_formatted_text(
                HTML(
                    "<ansired>No available LLM providers to switch to. Please add a provider first.</ansired>"
                )
            )
            return None

        provider_choice = choice(
            message="Select LLM provider to switch to:",
            options=available_model_options + [("x", "Cancel")],
            show_frame=~is_done,  # type: ignore
        )
        print()

        if provider_choice == "x":
            return None

        return available_providers[provider_choice]

    def select_agents_for_switch(self) -> list[str]:
        agent_options = [
            (agent.value, f"{agent.value.title()} Agent") for agent in SUPPORTED_AGENTS
        ]

        selected_agents = checkboxlist_dialog(
            title="Select Agents to Switch LLM Provider",
            text="Select which agents should use the newly selected LLM provider:",
            values=agent_options,
        ).run()
        print()
        if not selected_agents:
            print_formatted_text(
                HTML(
                    "<ansired>No agents selected. The LLM provider will not be switched for any agent.</ansired>"
                )
            )
            return []
        return [
            value
            for value in selected_agents
            if value in [agent.value for agent in SUPPORTED_AGENTS]
        ]

    def handle_mod_sys_prompt(self, current_sys_prompt: str = "") -> str:
        new_sys_prompt = prompt(
            HTML("Enter new system prompt: "), default=current_sys_prompt
        )
        if not new_sys_prompt.lstrip():
            print_formatted_text(
                HTML(
                    "<ansired>System prompt cannot be empty. Keeping the existing prompt.</ansired>"
                )
            )
            return current_sys_prompt
        return new_sys_prompt

    def handle_mod_user_prompt(self, current_user_prompt: str = "") -> str:
        new_user_prompt = prompt(
            HTML("Enter new user prompt: "), default=current_user_prompt
        )
        if not new_user_prompt.lstrip():
            print_formatted_text(
                HTML(
                    "<ansired>User prompt cannot be empty. Keeping the existing prompt.</ansired>"
                )
            )
            return current_user_prompt
        return new_user_prompt

    def handle_mod_tool_prompt(self, current_tool_prompt: str = "") -> str:
        new_tool_prompt = prompt(
            HTML("Enter new tool prompt: "), default=current_tool_prompt
        )
        if not new_tool_prompt.lstrip():
            print_formatted_text(
                HTML(
                    "<ansired>Tool prompt cannot be empty. Keeping the existing prompt.</ansired>"
                )
            )
            return current_tool_prompt
        return new_tool_prompt
