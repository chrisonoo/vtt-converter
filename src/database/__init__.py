"""
Database package for VTT Converter.
"""

from .connection import DatabaseConnection, create_tables, get_db_connection
from .repositories import (
    FileRepository,
    add_file,
    add_processed_file,
    get_pending_files,
    get_processed_files,
    update_file_status,
)

__all__ = [
    # Connection management
    "DatabaseConnection",
    "get_db_connection",
    "create_tables",
    # Repositories
    "FileRepository",
    # Legacy functions
    "add_file",
    "update_file_status",
    "add_processed_file",
    "get_pending_files",
    "get_processed_files",
]
