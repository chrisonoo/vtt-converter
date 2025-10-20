"""
Command Line Interface for VTT Converter.
"""

import argparse
import sys
from pathlib import Path

from src.config import config
from src.database import (
    add_processed_file,
    create_tables,
    get_pending_files,
    update_ai_content,
    update_file_status,
)
from src.services.file_service import FileService
from src.services.openai_client import OpenAIClient
from src.services.vtt_parser import parse_vtt_file


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

    # Initialize database and services
    create_tables()
    file_service = FileService()
    openai_client = OpenAIClient() if config.OPENAI_API_KEY else None

    try:
        # Discover and add VTT files to the database
        print("Discovering VTT files...")
        found_files = file_service.discover_vtt_files(str(args.directory))
        for file_path in found_files:
            print(f"Found file: {file_path}")
        print("File discovery complete.")

        # Process pending files
        print("Processing pending files...")
        pending_files = get_pending_files()
        for file_id, file_path, filename in pending_files:
            print(f"Processing {filename}...")
            cleaned_text = parse_vtt_file(file_path)
            full_content = "\n".join(cleaned_text)
            add_processed_file(file_id, full_content)

            if openai_client:
                print("Generating summary with OpenAI...")
                ai_content = openai_client.get_summary(full_content)
                update_ai_content(file_id, ai_content)
                md_path = Path(file_path).with_suffix(".md")
                with open(md_path, "w", encoding="utf-8") as md_file:
                    md_file.write(ai_content)
                print(f"Summary saved to {md_path}")

            update_file_status(file_id, 1)
            if config.LOGGING:
                print(full_content)
        print("File processing complete.")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
