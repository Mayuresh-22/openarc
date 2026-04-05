from hashlib import sha256
import os
import sys

from src.config.config import CWD_PATH


def build_session_id(seed: str = str(CWD_PATH)) -> str:
    """Idempotent session ID generator that produces the same session ID for the same seed input.
    By default, it uses the current working directory path as the seed"""
    return sha256(seed.encode()).hexdigest()


def build_environment_prompt() -> str:
    """Builds a prompt that describes the current environment, including the operating system and Python version."""
    os_info = f"Operating System: {os.name}"
    python_info = f"Python Version: {sys.version}"
    return f"{os_info}\n{python_info}"
