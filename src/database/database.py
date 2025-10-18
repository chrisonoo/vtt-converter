import sqlite3
from typing import List, Tuple

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect('vtt_converter.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Create the necessary tables in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL DEFAULT 'pending'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_text (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            FOREIGN KEY (file_id) REFERENCES files (id)
        )
    ''')

    conn.commit()
    conn.close()

def add_file(path: str):
    """Add a file to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO files (path) VALUES (?)", (path,))
        conn.commit()
    except sqlite3.IntegrityError:
        # File already exists
        pass
    finally:
        conn.close()

def update_file_status(file_id: int, status: str):
    """Update the status of a file."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE files SET status = ? WHERE id = ?", (status, file_id))
    conn.commit()
    conn.close()

def add_processed_text(file_id: int, texts: List[str]):
    """Add processed text to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    data = [(file_id, text) for text in texts]
    cursor.executemany("INSERT INTO processed_text (file_id, text) VALUES (?, ?)", data)
    conn.commit()
    conn.close()

def get_pending_files() -> List[Tuple[int, str]]:
    """Get all files with 'pending' status."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, path FROM files WHERE status = 'pending'")
    files = cursor.fetchall()
    conn.close()
    return [(row['id'], row['path']) for row in files]

if __name__ == '__main__':
    create_tables()
    print("Database tables created successfully.")
