"""
Database connection management for VTT Converter.
"""

import sqlite3
from contextlib import contextmanager


class DatabaseConnection:
    """Manages database connections and provides context managers."""

    def __init__(self, db_path: str = "vtt_converter.db"):
        """Initialize database connection manager.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        """Create and return a database connection with Row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @contextmanager
    def get_connection_context(self):
        """Context manager for database connections."""
        conn = None
        try:
            conn = self.get_connection()
            yield conn
        finally:
            if conn:
                conn.close()

    def create_tables(self) -> None:
        """Create the necessary tables in the database."""
        with self.get_connection_context() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL UNIQUE,
                    status TEXT NOT NULL DEFAULT 'pending'
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS processed_text (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_id INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    FOREIGN KEY (file_id) REFERENCES files (id)
                )
            """)

            conn.commit()


# Global instance for backward compatibility
_db_connection = DatabaseConnection()


def get_db_connection() -> sqlite3.Connection:
    """Create and return a database connection (legacy function)."""
    return _db_connection.get_connection()


def create_tables() -> None:
    """Create the necessary tables in the database (legacy function)."""
    _db_connection.create_tables()


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully.")
