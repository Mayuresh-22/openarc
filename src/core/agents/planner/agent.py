from agno.agent import Agent
from agno.db.sqlite import SqliteDb

from src.config.config import ConfigService
from src.core.agents.agent_config_service import AgentConfigService
from src.const.agents import ALL_AGENT_MEMORY_PATHS
from src.types.agents import PlannerAgentOutputSchema
from src.tools.registry import ToolRegistry
from src.utils.agent import build_environment_prompt, build_session_id


class PlannerAgent:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PlannerAgent, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        agent_config_service=AgentConfigService(config_service=ConfigService()),
        tool_registry=ToolRegistry(),
    ):
        self.agent_config_service = agent_config_service
        self.tool_registry = tool_registry
        self.session_id = build_session_id()

    def get_agent(self):
        self.agent_config = self.agent_config_service.get_agent_config("planner")
        self.planner_agent = Agent(
            name="Planner Agent",
            session_id=self.session_id,
            description=f"You are a OpenArc's planner agent. OpenArc is a dev focused CLI that plans, executes and verifies developer tasks from natural language. Extended description: <user_description>{self.agent_config.description}</user_description>",
            model=self.agent_config.model,
            instructions=[
                "You are OpenArc's Planner Agent.",
                "Your role is to transform a natural-language developer request into a logical, execution-ready step-by-step plan.",
                f"Available toolkits (use exact names only):\n{self.tool_registry.get_all_toolkits()}",
                f"Environment:\n{build_environment_prompt()}",
                "Each step must contain: step_name, step_description, tools_required (exact toolkit names or empty list), expected_output.",
                "Order steps by dependency. Use minimum toolkits per step. If the request can't be fulfilled, state why.",
            ],
            db=SqliteDb(ALL_AGENT_MEMORY_PATHS.PLANNER_AGENT),
            output_schema=PlannerAgentOutputSchema,
            # add_history_to_context=True,
            markdown=True,
            telemetry=False,
        )

        return self.planner_agent


planner_agent = PlannerAgent()
