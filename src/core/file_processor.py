"""
Core file processing logic for VTT Converter.
"""

from pathlib import Path

from src.utils.file_utils import find_vtt_files


class FileProcessor:
    """
    Core processor for VTT file operations.
    """

    def __init__(self) -> None:
        """Initialize the file processor."""
        pass

    def process_directory(self, directory: Path) -> list[Path]:
        """
        Process a directory to find subtitle files.

        Searches for all supported subtitle file extensions as configured.

        Args:
            directory: The directory to process

        Returns:
            List of found subtitle files

        Raises:
            ValueError: If directory validation fails
        """
        return find_vtt_files(directory)

    def format_file_list(self, files: list[Path], base_directory: Path) -> str:
        """
        Format a list of files for display.

        Args:
            files: List of file paths to format
            base_directory: Base directory for relative path calculation

        Returns:
            Formatted string representation of the file list
        """
        if not files:
            return "No subtitle files found."

        lines = [f"Found {len(files)} subtitle file(s):", ""]

        for i, vtt_file in enumerate(files, 1):
            try:
                relative_path = vtt_file.relative_to(base_directory)
            except ValueError:
                # If relative path calculation fails, use absolute path
                relative_path = vtt_file

            lines.append(f"{i}. {relative_path}")

        return "\n".join(lines)

    def display_search_header(self, directory: Path) -> str:
        """
        Generate the search header message.

        Args:
            directory: Directory being searched

        Returns:
            Formatted header string
        """
        return f"Searching for subtitle files in: {directory.absolute()}\n{'-' * 60}"
