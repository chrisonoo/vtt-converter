#!/usr/bin/env python3
"""
VTT Converter - A tool for processing VTT subtitle files.
"""

import argparse
import sys
from pathlib import Path


def find_vtt_files(directory: Path) -> list[Path]:
    """
    Recursively find all VTT files in the given directory.

    Args:
        directory: The directory to search in

    Returns:
        List of Path objects pointing to VTT files
    """
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        return []

    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory.")
        return []

    vtt_files = list(directory.rglob("*.vtt"))
    return sorted(vtt_files)


def list_vtt_files(directory: Path) -> None:
    """
    Find and display all VTT files in the given directory and its subdirectories.

    Args:
        directory: The directory to search in
    """
    print(f"Searching for VTT files in: {directory.absolute()}")
    print("-" * 60)

    vtt_files = find_vtt_files(directory)

    if not vtt_files:
        print("No VTT files found.")
        return

    print(f"Found {len(vtt_files)} VTT file(s):")
    print()

    for i, vtt_file in enumerate(vtt_files, 1):
        relative_path = vtt_file.relative_to(directory)
        print(f"{i}. {relative_path}")


def main():
    """Main entry point of the application."""
    parser = argparse.ArgumentParser(
        description="VTT Converter - Find and process VTT subtitle files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py /path/to/directory
  python main.py .
        """
    )

    parser.add_argument(
        "directory",
        type=Path,
        help="Directory to search for VTT files"
    )

    args = parser.parse_args()

    try:
        list_vtt_files(args.directory)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
