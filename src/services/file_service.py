"""
File service layer for VTT Converter.

This service coordinates file operations between the presentation layer and core business logic.
"""

import sys
from pathlib import Path

from src.core.file_processor import FileProcessor


class FileService:
    """
    Service layer for file operations.

    This service acts as an abstraction layer between the CLI/GUI and the core file
    processing logic. It handles high-level operations, error management, and coordinates multiple
    core components.
    """

    def __init__(self) -> None:
        """Initialize the file service with required components."""
        self.processor = FileProcessor()

    def list_subtitle_files(self, directory: Path) -> None:
        """
        Find and display all subtitle files in the given directory and its subdirectories.

        This is a high-level service method that coordinates the entire file listing operation.

        Args:
            directory: The directory to search in

        Raises:
            SystemExit: If an error occurs during processing
        """
        try:
            # Display search header
            header = self.processor.display_search_header(directory)
            print(header)

            # Process directory and find files
            subtitle_files = self.processor.process_directory(directory)

            # Format and display results
            result = self.processor.format_file_list(subtitle_files, directory)
            print(result)

        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)
