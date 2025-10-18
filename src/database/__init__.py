"""
Database package for VTT Converter.
"""

from .connection import DatabaseConnection, create_tables, get_db_connection
from .repositories import (
    FileRepository,
    ProcessedTextRepository,
    add_file,
    add_processed_text,
    get_pending_files,
    update_file_status,
)

__all__ = [
    # Connection management
    "DatabaseConnection",
    "get_db_connection",
    "create_tables",
    # Repositories
    "FileRepository",
    "ProcessedTextRepository",
    # Legacy functions
    "add_file",
    "update_file_status",
    "add_processed_text",
    "get_pending_files",
]
