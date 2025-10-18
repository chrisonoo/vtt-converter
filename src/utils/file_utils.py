"""
File utility functions for VTT Converter.
"""

from pathlib import Path


def find_files_by_extension(directory: Path, extension: str) -> list[Path]:
    """
    Recursively find all files with the specified extension in the given directory.

    Args:
        directory: The directory to search in
        extension: File extension to search for (without the dot, e.g., 'vtt')

    Returns:
        List of Path objects pointing to files with the specified extension

    Raises:
        ValueError: If directory does not exist or is not a directory
    """
    if not directory.exists():
        raise ValueError(f"Directory '{directory}' does not exist.")

    if not directory.is_dir():
        raise ValueError(f"'{directory}' is not a directory.")

    pattern = f"*.{extension}"
    files = list(directory.rglob(pattern))
    return sorted(files)


def find_vtt_files(directory: Path) -> list[Path]:
    """
    Recursively find all VTT files in the given directory.

    This is a convenience function for finding VTT files specifically.

    Args:
        directory: The directory to search in

    Returns:
        List of Path objects pointing to VTT files

    Raises:
        ValueError: If directory does not exist or is not a directory
    """
    return find_files_by_extension(directory, "vtt")
