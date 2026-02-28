from agno.agent import Agent
from agno.db.sqlite import SqliteDb

from src.config.config import ConfigService
from src.core.agents.agent_config_service import AgentConfigService
from src.const.agents import ALL_AGENT_MEMORY_PATHS
from src.types.agents import PlannerAgentOutputSchema


agent_config_service = AgentConfigService(config_service=ConfigService())
agent_config = agent_config_service.get_agent_config("planner")

planner_agent = Agent(
    name=agent_config.name or "Planner Agent",
    description=agent_config.description
    or "You are a OpenArc's planner agent. OpenArc is a dev focused CLI that plans, executes and verifies developer tasks from natural language.",
    model=agent_config.model,
    instructions=[
        "You will be given a task in natural language. Your job is to break down the task into smaller, manageable steps and create a plan to accomplish the main task.",
        "For each step, you should specify the following:",
        "- step name: A concise and descriptive name for the step.",
        "- step description: A clear and concise description of the step.",
        "- Tools required: List any tools or resources needed to complete the step.",
        "- Expected output: Describe the expected outcome or result of the step.",
        "Once you have broken down the main task into steps, you should organize them in a logical order, ensuring that dependencies between steps are clearly identified. Your final output should be a structured plan that outlines the steps needed to complete the main task, along with any necessary details for each step.",
        "Remember to keep your plan clear and concise, and ensure that it is actionable by the Executor Agent.",
    ],
    db=SqliteDb(ALL_AGENT_MEMORY_PATHS.PLANNER_AGENT),
    output_schema=PlannerAgentOutputSchema,
    add_history_to_context=True,
    telemetry=False,
)
