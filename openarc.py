from prompt_toolkit import HTML, print_formatted_text
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
from src.utils.print_style import print_with_frame, cli_style
from src.utils.prompt import prompt_session


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
            user_input = prompt_session.prompt(
                HTML("<input>> </input>"), style=cli_style
            )

            if user_input.strip().lower() in ["exit"]:
                exit(0)

            input_type = InputRouter().route_input(user_input)

            result = main_input_handler.handle(
                input_type.input_type, input_type.content
            )

            if result.stderr:
                print_formatted_text(
                    HTML(f"<error>{result.stderr}</error>"), style=cli_style
                )
            elif result.stdout:
                print_with_frame(
                    f"{result.stdout}", style=cli_style
                )
        except KeyboardInterrupt as e:
            print_formatted_text(
                HTML("<error>KeyboardInterrupt detected. Exiting...</error>"), style=cli_style
            )
            exit(0)
        except Exception as e:
            print_formatted_text(
                HTML(f"<error>Error: {str(e)}</error>"), style=cli_style
            )


if __name__ == "__main__":
    main_loop()
