from git import Optional
from src.config.config import ConfigService
from src.types.config import AvailableLLMProvider, SupportedLLMProvider


class LLMProviderRegistry:
    def __init__(self, config_service: ConfigService):
        self.registry = {}
        self.config_service = config_service

    def is_provider_registered(self, code_name: str, model_id: str) -> bool:
        for (
            provider_code_name,
            provider_model_id,
        ) in self.config_service.load_config().available_llm_providers_by_code_name:
            if provider_code_name == code_name and provider_model_id == model_id:
                return True
        return False

    def register_provider(self, llm_provider: AvailableLLMProvider):
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

        if not temp_config_file.current_llm_provider:
            self.set_current_provider(llm_provider)

    def set_current_provider(self, llm_provider: AvailableLLMProvider):
        temp_config_file = self.config_service.load_config()

        temp_config_file.current_llm_provider = AvailableLLMProvider(
            provider_name=llm_provider.provider_name,  # type: ignore
            code_name=llm_provider.code_name,  # type: ignore
            model_id=llm_provider.model_id,  # type: ignore
            api_key=llm_provider.api_key,  # type: ignore
        )

        self.config_service.save_config()

    def get_current_provider(self) -> Optional[AvailableLLMProvider]:
        current_provider = self.config_service.load_config().current_llm_provider
        if current_provider is None:
            return None
        return current_provider

    def get_supported_llm_providers(self) -> list[SupportedLLMProvider]:
        return self.config_service.load_config().supported_llm_providers

    def get_available_llm_providers(self) -> list[AvailableLLMProvider]:
        return self.config_service.load_config().available_llm_providers
