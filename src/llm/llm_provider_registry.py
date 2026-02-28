from src.core.agents.agent_config_service import AgentConfigService
from src.config.config import ConfigService
from src.types.config import AvailableLLMProvider, SupportedLLMProvider


class LLMProviderRegistry:
    _instance = None

    def __new__(cls, *args, **kwargs) -> "LLMProviderRegistry":
        if cls._instance is None:
            cls._instance = super(LLMProviderRegistry, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_service: ConfigService):
        self.config_service = config_service

    def is_provider_registered(self, code_name: str, model_id: str) -> bool:
        """
        Checks if a provider with the given code_name and model_id is registered in the loaded configuration. Returns True if found, otherwise False.
        """
        for (
            provider_code_name,
            provider_model_id,
        ) in self.config_service.load_config().available_llm_providers_by_code_name:
            if provider_code_name == code_name and provider_model_id == model_id:
                return True
        return False

    def register_llm_provider(self, llm_provider: AvailableLLMProvider):
        """
        Registers a new LLM provider in the configuration.
        """
        temp_config_file = self.config_service.load_config()

        temp_config_file.available_llm_providers.append(
            AvailableLLMProvider(
                provider_name=llm_provider.provider_name,  # type: ignore
                code_name=llm_provider.code_name,  # type: ignore
                model_id=llm_provider.model_id,  # type: ignore
                api_key=llm_provider.api_key,  # type: ignore
            )
        )
        temp_config_file.available_llm_providers_by_code_name.append(
            (llm_provider.code_name, llm_provider.model_id)  # type: ignore
        )

        self.config_service.save_config()

    def get_supported_llm_providers(self) -> list[SupportedLLMProvider]:
        """Returns a list of supported LLM providers from the configuration."""
        return self.config_service.load_config().supported_llm_providers

    def get_available_llm_providers(self) -> list[AvailableLLMProvider]:
        """Returns a list of available LLM providers from the configuration."""
        return self.config_service.load_config().available_llm_providers
