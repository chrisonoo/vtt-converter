"""
File utility functions for VTT Converter.
"""

from pathlib import Path

from src.config import SUPPORTED_EXTENSIONS


def find_files_by_extensions(directory: Path, extensions: list[str]) -> list[Path]:
    """
    Recursively find all files with the specified extensions in the given directory.

    Args:
        directory: The directory to search in
        extensions: List of file extensions to search for (without the dot, e.g., ['vtt', 'srt'])

    Returns:
        List of Path objects pointing to files with the specified extensions

    Raises:
        ValueError: If directory does not exist or is not a directory
    """
    if not directory.exists():
        raise ValueError(f"Directory '{directory}' does not exist.")

    if not directory.is_dir():
        raise ValueError(f"'{directory}' is not a directory.")

    files: list[Path] = []
    for extension in extensions:
        pattern = f"*.{extension}"
        files.extend(directory.rglob(pattern))

    return sorted(files)


def find_vtt_files(directory: Path) -> list[Path]:
    """
    Recursively find all VTT files in the given directory.

    This is a convenience function for finding VTT files specifically.
    Uses the configured supported extensions.

    Args:
        directory: The directory to search in

    Returns:
        List of Path objects pointing to VTT files

    Raises:
        ValueError: If directory does not exist or is not a directory
    """
    return find_files_by_extensions(directory, SUPPORTED_EXTENSIONS)
