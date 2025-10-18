"""
Repository layer for database operations in VTT Converter.
"""

import contextlib
import sqlite3

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
        with self.db.get_connection_context() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO files (path) VALUES (?)", (path,))
            conn.commit()

    def update_file_status(self, file_id: int, status: str) -> None:
        """Update the status of a file.

        Args:
            file_id: ID of the file to update
            status: New status for the file
        """
        with self.db.get_connection_context() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE files SET status = ? WHERE id = ?", (status, file_id))
            conn.commit()

    def get_pending_files(self) -> list[tuple[int, str]]:
        """Get all files with 'pending' status.

        Returns:
            List of tuples containing (file_id, file_path)
        """
        with self.db.get_connection_context() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, path FROM files WHERE status = 'pending'")
            files = cursor.fetchall()
            return [(row["id"], row["path"]) for row in files]

    def get_file_by_path(self, path: str) -> tuple[int, str, str] | None:
        """Get file information by path.

        Args:
            path: Path to the file

        Returns:
            Tuple of (id, path, status) or None if not found
        """
        with self.db.get_connection_context() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, path, status FROM files WHERE path = ?", (path,))
            row = cursor.fetchone()
            return (row["id"], row["path"], row["status"]) if row else None


class ProcessedTextRepository:
    """Repository for processed text database operations."""

    def __init__(self, db_connection: DatabaseConnection | None = None):
        """Initialize processed text repository.

        Args:
            db_connection: Database connection manager, uses default if None
        """
        self.db = db_connection or DatabaseConnection()

    def add_processed_text(self, file_id: int, texts: list[str]) -> None:
        """Add processed text to the database.

        Args:
            file_id: ID of the file this text belongs to
            texts: List of text strings to add
        """
        with self.db.get_connection_context() as conn:
            cursor = conn.cursor()
            data = [(file_id, text) for text in texts]
            cursor.executemany("INSERT INTO processed_text (file_id, text) VALUES (?, ?)", data)
            conn.commit()

    def get_processed_text_by_file_id(self, file_id: int) -> list[str]:
        """Get all processed text for a specific file.

        Args:
            file_id: ID of the file

        Returns:
            List of processed text strings
        """
        with self.db.get_connection_context() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT text FROM processed_text WHERE file_id = ?", (file_id,))
            rows = cursor.fetchall()
            return [row["text"] for row in rows]


# Global instances for backward compatibility
_file_repo = FileRepository()
_processed_text_repo = ProcessedTextRepository()


# Legacy functions for backward compatibility
def add_file(path: str) -> None:
    """Add a file to the database (legacy function)."""
    with contextlib.suppress(sqlite3.IntegrityError):
        _file_repo.add_file(path)


def update_file_status(file_id: int, status: str) -> None:
    """Update the status of a file (legacy function)."""
    _file_repo.update_file_status(file_id, status)


def add_processed_text(file_id: int, texts: list[str]) -> None:
    """Add processed text to the database (legacy function)."""
    _processed_text_repo.add_processed_text(file_id, texts)


def get_pending_files() -> list[tuple[int, str]]:
    """Get all files with 'pending' status (legacy function)."""
    return _file_repo.get_pending_files()
