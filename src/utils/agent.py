from hashlib import sha256

from src.config.config import CWD_PATH


def build_session_id(seed: str = str(CWD_PATH)) -> str:
    """Idempotent session ID generator that produces the same session ID for the same seed input. By default, it uses the current working directory path as the seed"""
    return sha256(seed.encode()).hexdigest()
