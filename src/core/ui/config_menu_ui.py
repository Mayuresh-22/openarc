from typing import Optional
from prompt_toolkit import HTML, choice, print_formatted_text, prompt
from prompt_toolkit.filters import is_done
from src.core.prompts.prompt import PromptService
from src.const.config import CONFIG_MENU_VAL_LABEL_MAP
from src.const.llm import SUPPORTED_MODEL_PROVIDERS
from src.types.config import AvailableLLMProvider, SupportedLLMProvider
from src.utils.prompt import prompt_session


class ConfigMenuUI:
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

    def handle_mod_sys_prompt(self, current_sys_prompt: str = "") -> str:
        new_sys_prompt = prompt(
            HTML("Enter new system prompt: "),
            default=current_sys_prompt
        )
        if not new_sys_prompt.lstrip():
            print_formatted_text(
                HTML("<ansired>System prompt cannot be empty. Keeping the existing prompt.</ansired>")
            )
            return current_sys_prompt
        return new_sys_prompt


    def handle_mod_user_prompt(self, current_user_prompt: str = "") -> str:
        new_user_prompt = prompt(
            HTML("Enter new user prompt: "),
            default=current_user_prompt
        )
        if not new_user_prompt.lstrip():
            print_formatted_text(
                HTML("<ansired>User prompt cannot be empty. Keeping the existing prompt.</ansired>")
            )
            return current_user_prompt
        return new_user_prompt

    def handle_mod_tool_prompt(self, current_tool_prompt: str = "") -> str:
        new_tool_prompt = prompt(
            HTML("Enter new tool prompt: "),
            default=current_tool_prompt
        )
        if not new_tool_prompt.lstrip():
            print_formatted_text(
                HTML("<ansired>Tool prompt cannot be empty. Keeping the existing prompt.</ansired>")
            )
            return current_tool_prompt
        return new_tool_prompt
