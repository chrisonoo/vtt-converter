"""
Configuration modules for VTT Converter.
"""

import os

from dotenv import load_dotenv

from .config import Config

# Only expose the list of supported extensions (recommended for clarity)
SUPPORTED_EXTENSIONS = Config.SUPPORTED_EXTENSIONS


def load_logging_config() -> bool:
    """
    Load logging configuration from .env file.

    Returns:
        True if logging is enabled, False otherwise.
    """
    load_dotenv()
    return os.getenv("LOGGING", "false").lower() == "true"


__all__ = [
    "SUPPORTED_EXTENSIONS",
    "load_logging_config",
]
