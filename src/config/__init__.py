"""
Configuration modules for VTT Converter.
"""

from .config import Config

# Only expose the list of supported extensions (recommended for clarity)
SUPPORTED_EXTENSIONS = Config.SUPPORTED_EXTENSIONS

__all__ = [
    "SUPPORTED_EXTENSIONS",
]
