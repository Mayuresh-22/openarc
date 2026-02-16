from pydantic import BaseModel
from os.path import dirname as up
import os


class SupportedModel(BaseModel):
    code_name: str
    name: str


class AvailableModel(BaseModel):
    provider_name: str
    model_id: str
    api_key: str


class ConfigType(BaseModel):
    supported_models: list[SupportedModel] = []
    available_models: list[AvailableModel] = []
    root_dir: str = os.path.join(up(up(up(__file__))))
