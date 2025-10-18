import os
from src.database.database import add_file

class FileService:
    """Service for handling file operations."""

    def discover_vtt_files(self, directory: str):
        """Discover all .vtt files in a directory and add them to the database."""
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.vtt'):
                    file_path = os.path.join(root, file)
                    add_file(file_path)
