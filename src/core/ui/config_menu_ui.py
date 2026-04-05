from typing import Optional
from src.const.agents import SUPPORTED_AGENTS
from src.core.prompts.prompt import PromptService
from src.const.config import CONFIG_MENU_VAL_LABEL_MAP
from src.const.llm import SUPPORTED_MODEL_PROVIDERS
from src.types.config import AvailableLLMProvider, SupportedLLMProvider
from src.utils.print_style import print_with_frame, CLI_COLORS, console


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
        print_with_frame("Select a configuration option:", color=CLI_COLORS["header"], style="header")
        options = list(CONFIG_MENU_VAL_LABEL_MAP.items())
        for idx, (key, value) in enumerate(options, 1):
            console.print(f"[bold cyan]{idx}.[/bold cyan] [white]{value}[/white]")
        choice_idx = console.input("[bold cyan]Enter choice number: [/bold cyan]")
        try:
            choice_idx = int(choice_idx)
            if 1 <= choice_idx <= len(options):
                return options[choice_idx - 1][0]
        except Exception:
            pass
        return None

    def handle_add_llm_provider(
        self,
    ) -> tuple[Optional[SupportedLLMProvider], Optional[str], Optional[str]]:
        print_with_frame("Enter LLM provider details:", color=CLI_COLORS["header"], style="header")
        for idx, (_, name) in enumerate(self.supported_llm_providers, 1):
            console.print(f"[bold cyan]{idx}.[/bold cyan] [white]{name}[/white]")
        console.print(f"[bold cyan]x.[/bold cyan] [white]Cancel[/white]")
        option_choice = console.input("[bold cyan]Enter choice number or x to cancel: [/bold cyan]")
        if option_choice == "x":
            return None, None, None
        try:
            option_choice = int(option_choice)
            if 1 <= option_choice <= len(self.supported_llm_providers):
                api_key = console.input("[bold cyan]Enter API key for the selected provider: [/bold cyan]")
                model_id = console.input("[bold cyan]Enter model ID to use (e.g. gpt-4): [/bold cyan]")
                return SUPPORTED_MODEL_PROVIDERS[option_choice - 1], api_key, model_id
        except Exception:
            pass
        return None, None, None

    def handle_switch_llm_provider(
        self, available_providers: list[AvailableLLMProvider]
    ) -> Optional[AvailableLLMProvider]:
        available_model_options = [
            (i, f"{provider.provider_name} ({provider.model_id})")
            for i, provider in enumerate(available_providers)
        ]
        if not available_model_options:
            print_with_frame("No available LLM providers to switch to. Please add a provider first.", color="red", style="error")
            return None
        for idx, (_, label) in enumerate(available_model_options, 1):
            console.print(f"[bold cyan]{idx}.[/bold cyan] [white]{label}[/white]")
        console.print(f"[bold cyan]x.[/bold cyan] [white]Cancel[/white]")
        provider_choice = console.input("[bold cyan]Enter choice number or x to cancel: [/bold cyan]")
        if provider_choice == "x":
            return None
        try:
            provider_choice = int(provider_choice)
            if 1 <= provider_choice <= len(available_model_options):
                return available_providers[provider_choice - 1]
        except Exception:
            pass
        return None

    def select_agents_for_switch(self) -> list[str]:
        agent_options = [
            (agent.value, f"{agent.value.title()} Agent") for agent in SUPPORTED_AGENTS
        ]
        print_with_frame("Select Agents to Switch LLM Provider", color=CLI_COLORS["header"], style="header")
        for idx, (value, label) in enumerate(agent_options, 1):
            console.print(f"[bold cyan]{idx}.[/bold cyan] [white]{label}[/white]")
        console.print(f"[bold cyan]x.[/bold cyan] [white]Cancel[/white]")
        selected = console.input("[bold cyan]Enter agent numbers separated by comma, or x to cancel: [/bold cyan]")
        if selected.strip().lower() == "x":
            return []
        try:
            indices = [int(i.strip()) for i in selected.split(",") if i.strip().isdigit()]
            return [agent_options[i-1][0] for i in indices if 1 <= i <= len(agent_options)]
        except Exception:
            return []

    def handle_mod_sys_prompt(self, current_sys_prompt: str = "") -> str:
        new_sys_prompt = console.input(f"[bold cyan]Enter new system prompt (leave blank to keep current): [/bold cyan]")
        if not new_sys_prompt.lstrip():
            print_with_frame("System prompt cannot be empty. Keeping the existing prompt.", color="red", style="error")
            return current_sys_prompt
        return new_sys_prompt

    def handle_mod_user_prompt(self, current_user_prompt: str = "") -> str:
        new_user_prompt = console.input(f"[bold cyan]Enter new user prompt (leave blank to keep current): [/bold cyan]")
        if not new_user_prompt.lstrip():
            print_with_frame("User prompt cannot be empty. Keeping the existing prompt.", color="red", style="error")
            return current_user_prompt
        return new_user_prompt

    def handle_mod_tool_prompt(self, current_tool_prompt: str = "") -> str:
        new_tool_prompt = console.input(f"[bold cyan]Enter new tool prompt (leave blank to keep current): [/bold cyan]")
        if not new_tool_prompt.lstrip():
            print_with_frame("Tool prompt cannot be empty. Keeping the existing prompt.", color="red", style="error")
            return current_tool_prompt
        return new_tool_prompt
