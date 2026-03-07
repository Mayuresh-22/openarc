"""
This is the Planner agent runner. 

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

import json

from agno.workflow import StepInput, StepOutput
from prompt_toolkit import HTML, print_formatted_text, prompt
from pydantic import ValidationError
from src.core.agents.planner.agent import planner_agent
from src.utils.print_style import cli_style
from src.types.agents import PlannerAgentOutputSchema


def run_planner_agent(step_input: StepInput) -> StepOutput:
    planner_input = build_planner_agent_input(step_input)
    run_response = planner_agent.get_agent().run(planner_input, stream=True)
    fin_content = ""

    print_formatted_text(
        HTML("<header>Planner Agent Output:</header>"),
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
                run_response = planner_agent.get_agent().continue_run(
                    run_id=run_event.run_id,
                    requirements=run_event.requirements,  # type: ignore
                    stream=True,
                )
                break  # Re-enter while loop with new `run_response` object

            else:
                try:
                    event_content = PlannerAgentOutputSchema.model_validate(run_event.content)  # type: ignore
                    fin_content += json.dumps(event_content.model_dump()) or ""
                    event_content = event_content
                except ValidationError as e:
                    print(f"Failed to parse planner agent output: {e}")
                    if isinstance(run_event.content, str):
                        fin_content += run_event.content or ""
                        event_content = run_event.content or ""
                    else:
                        fin_content += str(run_event.content) or ""
                        event_content = str(run_event.content) or ""

                print_planner_agent_output(event_content)
        if not paused:
            break

    return StepOutput(content=fin_content)


def build_planner_agent_input(step_input: StepInput):
    # simpler for now; TODO: can be more sturcured.
    return f"User Task: {step_input.get_input_as_string()}"


def print_planner_agent_output(event_content: str | PlannerAgentOutputSchema):
    if isinstance(event_content, PlannerAgentOutputSchema):
        for step in event_content.plan:
            print_formatted_text(
                HTML(f"<output-bold>{step.step_name}</output-bold>"),
                style=cli_style
            )
            print_formatted_text(
                HTML(f"<grey>  Description: {step.step_description}</grey>"),
                style=cli_style
            )
            print_formatted_text(
                HTML("<grey>  Tools Required: " + ", ".join(step.tools_required) + "</grey>"),
                style=cli_style
            )
            # print_formatted_text(
            #     HTML(f"<grey>  Expected Output: {step.expected_output}</grey>"),
            #     style=cli_style
            # )
