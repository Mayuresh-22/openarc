from typing import Literal, Optional

from agno.models.base import Model
from agno.models.openai import OpenAIResponses
from agno.models.cerebras import Cerebras
from agno.models.groq import Groq
from agno.models.ollama import Ollama

from src.config.config import ConfigService
from src.types.config import AgentConfig, AvailableLLMProvider


class AgentConfigService:
    _instance = None

    def __new__(cls, *args, **kwargs) -> "AgentConfigService":
        if cls._instance is None:
            cls._instance = super(AgentConfigService, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_service: ConfigService):
        self.config_service = config_service

    def llm_provider_to_model(self, llm_provider: AvailableLLMProvider):
        """Helper method to convert an AvailableLLMProvider
        to the corresponding Agno compatible Model instance."""

        code_name = llm_provider.code_name
        if code_name == "openai":
            return OpenAIResponses(
                id=llm_provider.model_id, api_key=llm_provider.api_key
            )
        elif code_name == "cerebras":
            return Cerebras(id=llm_provider.model_id, api_key=llm_provider.api_key)
        elif code_name == "groq":
            return Groq(id=llm_provider.model_id, api_key=llm_provider.api_key)
        elif code_name == "ollama":
            return Ollama(id=llm_provider.model_id)
        else:
            raise ValueError(
                f"Unsupported LLM provider code name: {llm_provider.code_name}"
            )

    def get_agent_config(
        self, agent_name: Literal["planner", "executor", "verifier"]
    ) -> AgentConfig:
        return self.config_service.load_config().agents[agent_name]

    def set_agent_model(
        self,
        agent_name: Literal["planner", "executor", "verifier"],
        llm_provider: AvailableLLMProvider,
    ) -> None:
        print(
            f"Setting model for {agent_name.title()} Agent to {llm_provider.provider_name} ({llm_provider.model_id})..."
        )
        temp_config_file = self.config_service.load_config()
        temp_config_file.agents[agent_name].model = self.llm_provider_to_model(
            llm_provider
        )
        self.config_service.save_config()
