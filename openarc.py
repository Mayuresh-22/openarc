from src.core.agents.agent_config_service import AgentConfigService
from src.core.prompts.prompt import PromptService
from src.llm.llm_provider_registry import LLMProviderRegistry
from src.config.config import ConfigService
from src.core.handlers.arc_command_handler import ArcCommandHandler
from src.core.handlers.arc_query_handler import ArcQueryHandler
from src.core.handlers.main_input_handler import MainInputHandler
from src.core.handlers.shell_command_handler import ShellCommandHandler
from src.core.ui.config_menu_ui import ConfigMenuUI
from src.core.router.router import InputRouter
from src.utils.print_style import (
    CLI_COLORS, console
)


def main_loop():
    main_input_handler = MainInputHandler(
        shell_command_handler=ShellCommandHandler(),
        arc_command_handler=ArcCommandHandler(
            config_menu_ui_handler=ConfigMenuUI(),
            llm_provider_registry=LLMProviderRegistry(config_service=ConfigService()),
            agent_config_service=AgentConfigService(config_service=ConfigService()),
            prompt_service=PromptService()
        ),
        arc_query_handler=ArcQueryHandler(),
    )

    # print(planner_agent.run("create readme.md file for existing project", stream=False).content)

    while True:
        try:
            user_input = console.input(f"[{CLI_COLORS['input']}]> [{CLI_COLORS['input']}]").strip()

            if user_input.strip().lower() in ["exit"]:
                exit(0)

            input_type = InputRouter().route_input(user_input)

            result = main_input_handler.handle(
                input_type.input_type, input_type.content
            )

            if result.stderr:
                console.print(f"[{CLI_COLORS['error']}]{result.stderr}[{CLI_COLORS['error']}]")
            elif result.stdout:
                console.print(f"[{CLI_COLORS['output']}]${result.stdout}[{CLI_COLORS['output']}]")
        except KeyboardInterrupt as e:
            console.print(f"[{CLI_COLORS['error']}]KeyboardInterrupt detected. Exiting...[{CLI_COLORS['error']}]")
            exit(0)
        except Exception as e:
            console.print(f"[{CLI_COLORS['error']}]Error: {str(e)}[{CLI_COLORS['error']}]")


if __name__ == "__main__":
    main_loop()
