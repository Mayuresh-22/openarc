from typing import Optional
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


class ConfigFileType(BaseModel):
    available_llm_providers: list[AvailableLLMProvider]
    available_llm_providers_by_code_name: list[tuple[str, str]]
    current_llm_provider: Optional[AvailableLLMProvider]
    root_dir: str = os.path.join(up(up(up(__file__))))
    supported_llm_providers: list[SupportedLLMProvider]
