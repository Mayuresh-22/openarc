from agno.agent import Agent
from agno.db.sqlite import SqliteDb

from src.hooks.tool_hooks.logging import logging_hook
from src.config.config import ConfigService
from src.core.agents.agent_config_service import AgentConfigService
from src.const.agents import ALL_AGENT_MEMORY_PATHS
from src.types.agents import ExecutorAgentOutputSchema
from src.tools.registry import ToolRegistry
from src.utils.agent import build_session_id


class ExecutorAgent:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExecutorAgent, cls).__new__(cls)
        return cls._instance
    
    def __init__(
            self, 
            agent_config_service = AgentConfigService(config_service=ConfigService()),
            tool_registry = ToolRegistry()
        ):
        self.agent_config_service = agent_config_service
        self.tool_registry = tool_registry
        self.session_id = build_session_id()


    def get_agent(self):
        self.agent_config = self.agent_config_service.get_agent_config("executor")
        available_toolkits = self.tool_registry.get_all_toolkits()
        available_toolkit_names = [toolkit.__class__.__name__ for toolkit in available_toolkits]
        available_toolkits_text = "\n".join(f"- {name}" for name in available_toolkit_names)
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
                "You receive a structured plan consisting of ordered steps, each with a step_name, step_description, tools_required, and expected_output.",
                f"Available toolkits for execution:\n{available_toolkits_text}",
                "You must only use toolkits from the list above. Do not invent, rename, or generalize toolkit names.",
                "For each step:",
                "- Carefully read the step_name and step_description to understand the task.",
                "- Use only the toolkits listed in tools_required for that step. If tools_required is empty, perform the step without tool usage.",
                "- Execute steps strictly in the provided order, respecting dependencies.",
                "- After executing a step, verify that the expected_output matches the actual result as closely as possible.",
                "- If a step cannot be completed with the available toolkits, report the limitation clearly and do not attempt to improvise.",
                "- Do not perform any action outside the scope of the plan or the available toolkits.",
                "- Provide concise, actionable feedback for each step, including any errors or confirmations required (Use UserControlFlowToolkit to get user input when information is needed).",
                "Your output must be clear, deterministic, and directly usable by the verifier agent."
            ],
            add_history_to_context=True,
            markdown=True,
            tool_call_limit=50,
            telemetry=False
        )
        return self.executor_agent


executor_agent = ExecutorAgent()
