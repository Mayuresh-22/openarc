from agno.agent import Agent
from agno.db.sqlite import SqliteDb

from src.config.config import ConfigService
from src.core.agents.agent_config_service import AgentConfigService
from src.const.agents import ALL_AGENT_MEMORY_PATHS
from src.types.agents import PlannerAgentOutputSchema
from src.tools.registry import ToolRegistry


class PlannerAgent:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PlannerAgent, cls).__new__(cls)
        return cls._instance
    
    def __init__(
            self, 
            agent_config_service = AgentConfigService(config_service=ConfigService()),
            tool_registry = ToolRegistry()
        ):
        self.agent_config_service = agent_config_service
        self.tool_registry = tool_registry

    def get_agent(self):
        self.agent_config = self.agent_config_service.get_agent_config("planner")
        self.planner_agent = Agent(
            name=self.agent_config.name or "Planner Agent",
            description=f"You are a OpenArc's planner agent. OpenArc is a dev focused CLI that plans, executes and verifies developer tasks from natural language. Extended description: <user_description>{self.agent_config.description}</user_description>",
            model=self.agent_config.model,
            instructions=[
                "You are OpenArc's Planner Agent.",
                "Your role is to transform a natural-language developer request into a logical, execution-ready step-by-step plan.",
                f"Available toolkits:\n{self.tool_registry.get_all_toolkits()}",
                "You must analyze the available toolkits before creating the plan.",
                "You must only reference toolkit names exactly as listed above.",
                "Do not hallucinate, rename, or invent toolkit names.",
                "If a step does not need any toolkit, use an empty tools_required list.",
                "Break the task into the smallest logical steps needed to complete it.",
                "Order the steps so that dependencies are respected.",
                "Each step must contain:",
                "1. step_name: a descriptive name (displayed in CLI, inc step number)",
                "2. step_description: a brief actionable description",
                "3. tools_required: exact toolkit names from the available toolkit list only",
                "4. expected_output: the concrete outcome expected from the step",
                "Choose the minimum real toolkit set required for each step.",
                "Do not assign tools casually or speculatively.",
                "If the request cannot be completed using the available toolkits, reflect that clearly in the plan instead of inventing capabilities.",
                "Your output must be concise, logical, dependency-aware, and directly usable by the Executor Agent."
            ],
            db=SqliteDb(ALL_AGENT_MEMORY_PATHS.PLANNER_AGENT),
            output_schema=PlannerAgentOutputSchema,
            add_history_to_context=True,
            markdown=True,
            tool_call_limit=10,
            telemetry=False
        )

        return self.planner_agent

planner_agent = PlannerAgent()
