"""
OpenAI API client for VTT Converter.
"""

import openai
from src.config import config


class OpenAIClient:
    """Client for interacting with the OpenAI API."""

    def __init__(self):
        """Initialize the OpenAI client."""
        if not config.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not found in configuration.")
        openai.api_key = config.OPENAI_API_KEY

    def get_summary(self, content: str) -> str:
        """
        Get a summary from the OpenAI API.

        Args:
            content: The text content to summarize.

        Returns:
            The summarized text.
        """
        try:
            response = openai.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": config.AI_PROMPT},
                    {"role": "user", "content": content},
                ],
                temperature=config.OPENAI_TEMPERATURE,
            )
            if response.choices:
                return response.choices[0].message.content.strip()
            return "No summary generated."
        except openai.APIError as e:
            return f"OpenAI API error: {e}"
