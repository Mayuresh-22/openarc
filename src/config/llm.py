from src.types.config import SupportedLLMProvider


SUPPORTED_MODEL_PROVIDERS: list[SupportedLLMProvider] = [
    SupportedLLMProvider(code_name="openai", name="OpenAI"),
    SupportedLLMProvider(code_name="cerebras", name="Cerebras"),
    SupportedLLMProvider(code_name="groq", name="Groq"),
    SupportedLLMProvider(code_name="ollama", name="Ollama"),
]
