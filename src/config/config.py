"""
Application configuration.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for the application."""

    SUPPORTED_EXTENSIONS: list[str] = ["vtt"]
    AI_PROMPT: str = os.getenv("AI_PROMPT", "Summarize the following text:")
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-mini")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", 0.7))
