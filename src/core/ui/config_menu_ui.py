from prompt_toolkit import HTML, choice, prompt
from prompt_toolkit.filters import is_done
from src.config.llm import SUPPORTED_MODEL_PROVIDERS


class ConfigMenuUI:
    def __init__(self) -> None:
        self.supported_models = [
            (i, model.name) for i, model in enumerate(SUPPORTED_MODEL_PROVIDERS)
        ]

    def display_config_menu(self):
        menu_choice = choice(
            message="Select a configuration option:",
            options=[
                ("1", "Add LLM Provider"),
                ("2", "Switch LLM Provider"),
                ("3", "Back to Main Menu"),
            ],
            show_frame=~is_done,
            bottom_toolbar=HTML(
                " Press <b>[Up]</b>/<b>[Down]</b> to select, <b>[Enter]</b> to accept."
            ),
        )
        return menu_choice

    def handle_add_llm_provider(self):
        model_choice = choice(
            message="Enter LLM provider details:",
            options=self.supported_models + [("x", "Cancel")],
            show_frame=~is_done,
        )

        print()
        if model_choice == "x":
            return None, None, None

        _api_key = prompt(
            HTML("Enter API key for the selected provider: "),
            placeholder="sk-aQasd...",
            is_password=True,
        )
        _model_id = prompt(
            HTML("Enter model ID to use (e.g. gpt-4): "), placeholder="gpt-4"
        )
        return model_choice, _api_key, _model_id
