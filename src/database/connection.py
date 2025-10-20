"""
Database connection management for VTT Converter.
"""

import sqlite3
from contextlib import contextmanager, suppress
from pathlib import Path


class DatabaseConnection:
    """Manages database connections and provides context managers."""

    def __init__(self, db_path: str | None = None):
        """Initialize database connection manager.

        Args:
            db_path: Path to the SQLite database file. If None, uses default tmp/vtt.db
        """
        if db_path is None:
            # Default path: tmp/vtt.db relative to the application root
            app_root = Path(__file__).parent.parent.parent
            db_dir = app_root / "tmp"
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(db_dir / "vtt.db")

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

            # Create files table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL UNIQUE,
                    filename TEXT NOT NULL,
                    status INTEGER NOT NULL DEFAULT 0,
                    full_content TEXT
                )
            """)

            # Add filename column to existing tables if it doesn't exist
            with suppress(sqlite3.OperationalError):
                cursor.execute("ALTER TABLE files ADD COLUMN filename TEXT")

            # Update existing records to populate filename column
            cursor.execute("""
                UPDATE files
                SET filename = CASE
                    WHEN filename IS NULL THEN
                        substr(path, instr(path, '\\') + 1)
                    ELSE filename
                END
                WHERE filename IS NULL OR filename = ''
            """)

            # Migrate status column from TEXT to INTEGER (0=pending, 1=processed)
            # Check if status column is still TEXT type (old schema)
            cursor.execute("PRAGMA table_info(files)")
            columns = cursor.fetchall()
            status_column = next((col for col in columns if col[1] == "status"), None)

            if status_column and status_column[2] == "TEXT":
                # Migrate status column to INTEGER
                cursor.execute("ALTER TABLE files ADD COLUMN status_new INTEGER DEFAULT 0")
                cursor.execute("""
                    UPDATE files
                    SET status_new = CASE
                        WHEN status = 'pending' THEN 0
                        WHEN status = '1' THEN 1
                        WHEN CAST(status AS INTEGER) = 1 THEN 1
                        ELSE 0
                    END
                """)
                cursor.execute("ALTER TABLE files DROP COLUMN status")
                cursor.execute("ALTER TABLE files RENAME COLUMN status_new TO status")

            # Add full_content column to existing tables if it doesn't exist
            with suppress(sqlite3.OperationalError):
                cursor.execute("ALTER TABLE files ADD COLUMN full_content TEXT")

            # Migrate processed_files data to files table and drop the old table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='processed_files'")
            if cursor.fetchone():
                # Copy data from processed_files to files
                cursor.execute("""
                    UPDATE files
                    SET full_content = (
                        SELECT pf.full_content
                        FROM processed_files pf
                        WHERE pf.file_id = files.id
                    )
                    WHERE id IN (SELECT file_id FROM processed_files)
                """)
                # Drop the old table
                cursor.execute("DROP TABLE processed_files")

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
