"""
Command Line Interface for VTT Converter.
"""

import argparse
import sys
from pathlib import Path

from src.services.file_service import FileService


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="VTT Converter - Find and process subtitle files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py /path/to/directory
  python main.py .
        """,
    )

    parser.add_argument("directory", type=Path, help="Directory to search for subtitle files")

    return parser


def main() -> None:
    """
    Main CLI entry point.

    Parses command line arguments and executes the appropriate action.
    """
    parser = create_parser()
    args = parser.parse_args()

    # Initialize service
    file_service = FileService()

    try:
        # Execute the main operation
        file_service.list_subtitle_files(args.directory)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
