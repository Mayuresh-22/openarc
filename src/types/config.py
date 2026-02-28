from agno.models.cerebras import Cerebras
from agno.models.ollama import Ollama
from agno.models.groq import Groq
from agno.models.openai import OpenAIResponses

from typing import Literal, Optional
from pydantic import BaseModel
from os.path import dirname as up
import os


class SupportedLLMProvider(BaseModel):
    code_name: str
    name: str


class AvailableLLMProvider(BaseModel):
    provider_name: str
    code_name: str
    model_id: str
    api_key: str


class CurrentLLMProvider(BaseModel):
    provider_name: str
    code_name: str
    model_id: str


class AgentConfig(BaseModel):
    name: str
    model: Optional[Cerebras | Ollama | Groq | OpenAIResponses] = None
    description: str = ""
    model_config = {"arbitrary_types_allowed": True}


class ConfigFileType(BaseModel):
    agents: dict[Literal["planner", "executor", "verifier"], AgentConfig] = {
        "planner": AgentConfig(name="Planner Agent"),
        "executor": AgentConfig(name="Executor Agent"),
        "verifier": AgentConfig(name="Verifier Agent"),
    }
    available_llm_providers: list[AvailableLLMProvider] = []
    available_llm_providers_by_code_name: list[tuple[str, str]] = []
    root_dir: str = os.path.join(up(up(up(__file__))))
    supported_llm_providers: list[SupportedLLMProvider] = []
