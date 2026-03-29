"""
This is the Executor agent runner. 

what it does?
This runner runs the agent directly as custom function step in the agno workflow, 
handling HITL loop in the function step itself.
It supports both `requires_confirmation` and `dynamic user input` 
interactions for tool execution. 
The agent will pause and wait for user input when either of these conditions are met 
before proceeding with the execution of the tool.

Why?
Note: This is the workaround as agent tool level HITL is NOT propagated to the workflow in agno. 
This implementation ensures workflow execution is paused until the agent receives the necessary user input.
"""
from agno.workflow import StepInput, StepOutput
from prompt_toolkit import HTML, print_formatted_text, prompt
from pydantic import ValidationError
import regex
from src.core.agents.executor.agent import executor_agent
from src.utils.print_style import cli_style
from src.types.agents import ExecutorAgentOutputSchema


def run_executor_agent(step_input: StepInput) -> StepOutput:
    executor_input = build_executor_agent_input(step_input)
    run_response = executor_agent.get_agent().run(executor_input, stream=True)
    fin_content = ""

    print_formatted_text(
        HTML("<header>\n===== Executor Agent Output: =====</header>"),
        style=cli_style
    )
    while True:
        paused = False
        for run_event in run_response:
            if run_event.is_paused:
                paused = True
                for requirement in run_event.active_requirements:  # type: ignore
                    if requirement.needs_user_input:
                        print_formatted_text(
                            HTML("<confirm>Agent needs input:</confirm>"),
                            style=cli_style
                        )
                        for field in requirement.user_input_schema:  # type: ignore
                            if field.value is None:
                                field.value = prompt(
                                    HTML(f"  <confirm>{field.description or field.name}:</confirm> "),
                                    style=cli_style
                                )
                            else:
                                print_formatted_text(
                                    HTML(f"  <feedback-info>{field.name} (pre-filled): {field.value}</feedback-info>"),
                                    style=cli_style
                                )

                    elif requirement.needs_confirmation:
                        tool_exec = requirement.tool_execution  # type: ignore
                        print_formatted_text(
                            HTML(
                                f"<confirm>Confirm tool '{tool_exec.tool_name}' usage:</confirm> "  # type: ignore
                            ),
                            style=cli_style
                        )
                        print_formatted_text(
                            HTML(f"  <confirm>Args: {tool_exec.tool_args}</confirm>"),  # type: ignore
                            style=cli_style
                        )
                        answer = prompt(
                            HTML("  <confirm>Confirm? [y/N]:</confirm> "),
                            style=cli_style
                        ).strip().lower()
                        if answer == "y":
                            requirement.confirm()
                        else:
                            requirement.reject("Tool usage rejected by user")

                # Continue and loop back
                run_response = executor_agent.get_agent().continue_run(
                    run_id=run_event.run_id,
                    requirements=run_event.requirements,  # type: ignore
                    stream=True,
                )
                break  # Re-enter while loop with new `run_response` object
            else:
                if isinstance(run_event.content, str):
                    fin_content += run_event.content or ""
                    event_content = run_event.content or ""
                else:
                    fin_content += str(run_event.content) or ""
                    event_content = str(run_event.content) or ""

                print_executor_agent_output(event_content)
        if not paused:
            break

    return StepOutput(content=fin_content)


def build_executor_agent_input(step_input: StepInput):
    # simpler for now; TODO: can be more sturcured.
    return f"Task and generated plan: {step_input.get_input_as_string()}"


def print_executor_agent_output(event_content: str | ExecutorAgentOutputSchema):
    # remove trailing newlines for cleaner CLI output
    valid_output = regex.sub(r"\n+$", "", event_content) if isinstance(event_content, str) else event_content
    if isinstance(event_content, str):
        print_formatted_text(
            HTML(f"<grey>{valid_output}</grey>"),
            style=cli_style,
            end=""
        )
