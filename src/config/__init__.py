"""
Configuration loader for VTT Converter.
"""
from dotenv import load_dotenv
import os

def load_logging_config() -> bool:
    """
    Load logging configuration from .env file.

    Returns:
        True if logging is enabled, False otherwise.
    """
    load_dotenv()
    return os.getenv("LOGGING", "false").lower() == "true"
