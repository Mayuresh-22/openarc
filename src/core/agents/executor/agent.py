from agno.agent import Agent
from agno.db.sqlite import SqliteDb

from src.hooks.tool_hooks.logging import logging_hook
from src.config.config import ConfigService
from src.core.agents.agent_config_service import AgentConfigService
from src.const.agents import ALL_AGENT_MEMORY_PATHS
from src.types.agents import ExecutorAgentOutputSchema
from src.tools.registry import ToolRegistry
from src.utils.agent import build_environment_prompt, build_session_id


class ExecutorAgent:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExecutorAgent, cls).__new__(cls)
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
        self.agent_config = self.agent_config_service.get_agent_config("executor")
        available_toolkits = self.tool_registry.get_all_toolkits()
        available_toolkit_names = [
            toolkit.__class__.__name__ for toolkit in available_toolkits
        ]
        available_toolkits_text = "\n".join(
            f"- {name}" for name in available_toolkit_names
        )
        self.executor_agent = Agent(
            name="Executor Agent",
            session_id=self.session_id,
            description=f"You are OpenArc's executor agent. OpenArc is a dev-focused CLI that plans, executes, and verifies developer tasks from natural language. Your job is to execute each step in the provided plan using the available toolkits. Extended description: <user_description>{self.agent_config.description}</user_description>",
            model=self.agent_config.model,
            tools=available_toolkits,
            tool_hooks=[logging_hook],
            db=SqliteDb(ALL_AGENT_MEMORY_PATHS.EXECUTOR_AGENT),
            # output_schema=ExecutorAgentOutputSchema,
            instructions=[
                "You are OpenArc's Executor Agent.",
                "Your role is to execute the provided plan step-by-step in order, respecting dependencies.",
                f"Available toolkits (use only these):\n{available_toolkits_text}",
                f"Environment:\n{build_environment_prompt()}",
                "For each step: use only its tools_required, verify expected_output matches actual result, report limitations clearly.",
                "Use UserControlFlowToolkit when user input is needed. Be concise.",
                "Use correct spacing and markdown fomatting for readability."
            ],
            add_history_to_context=True,
            num_history_runs=5,
            compress_tool_results=True,
            tool_call_limit=50,
            markdown=True,
            telemetry=False,
        )
        return self.executor_agent


executor_agent = ExecutorAgent()
