"""
Repository layer for database operations in VTT Converter.
"""

import contextlib
import sqlite3
from pathlib import Path

from .connection import DatabaseConnection


class FileRepository:
    """Repository for file-related database operations."""

    def __init__(self, db_connection: DatabaseConnection | None = None):
        """Initialize file repository.

        Args:
            db_connection: Database connection manager, uses default if None
        """
        self.db = db_connection or DatabaseConnection()

    def add_file(self, path: str) -> None:
        """Add a file to the database.

        Args:
            path: Path to the file to add

        Raises:
            sqlite3.IntegrityError: If file already exists
        """
        filename = Path(path).name
        with self.db.get_connection_context() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO files (path, filename) VALUES (?, ?)", (path, filename))
            conn.commit()

    def update_file_status(self, file_id: int, status: str | int) -> None:
        """Update the status of a file.

        Args:
            file_id: ID of the file to update
            status: New status for the file
        """
        with self.db.get_connection_context() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE files SET status = ? WHERE id = ?", (status, file_id))
            conn.commit()

    def get_pending_files(self) -> list[tuple[int, str, str]]:
        """Get all files with pending status (status = 0).

        Returns:
            List of tuples containing (file_id, file_path, filename)
        """
        with self.db.get_connection_context() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, path, filename FROM files WHERE status = 0")
            files = cursor.fetchall()
            return [(row["id"], row["path"], row["filename"]) for row in files]

    def get_file_by_path(self, path: str) -> tuple[int, str, str, str] | None:
        """Get file information by path.

        Args:
            path: Path to the file

        Returns:
            Tuple of (id, path, filename, status) or None if not found
        """
        with self.db.get_connection_context() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, path, filename, status FROM files WHERE path = ?", (path,))
            row = cursor.fetchone()
            return (row["id"], row["path"], row["filename"], row["status"]) if row else None


# Global instances for backward compatibility
_file_repo = FileRepository()


class ProcessedFileRepository:
    """Repository for processed file database operations."""

    def __init__(self, db_connection: DatabaseConnection | None = None):
        """Initialize processed file repository.

        Args:
            db_connection: Database connection manager, uses default if None
        """
        self.db = db_connection or DatabaseConnection()

    def add_processed_file(self, file_id: int, full_content: str) -> None:
        """Add a processed file to the database.

        Args:
            file_id: ID of the file this content belongs to
            full_content: Full content of the processed file
        """
        with self.db.get_connection_context() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO processed_files (file_id, full_content) VALUES (?, ?)",
                (file_id, full_content),
            )
            conn.commit()


_processed_file_repo = ProcessedFileRepository()


def add_processed_file(file_id: int, full_content: str) -> None:
    """Add a processed file to the database (legacy function)."""
    _processed_file_repo.add_processed_file(file_id, full_content)


# Legacy functions for backward compatibility
def add_file(path: str) -> None:
    """Add a file to the database (legacy function)."""
    with contextlib.suppress(sqlite3.IntegrityError):
        _file_repo.add_file(path)


def update_file_status(file_id: int, status: str | int) -> None:
    """Update the status of a file (legacy function)."""
    _file_repo.update_file_status(file_id, status)


def get_pending_files() -> list[tuple[int, str, str]]:
    """Get all files with 'pending' status (legacy function)."""
    return _file_repo.get_pending_files()
