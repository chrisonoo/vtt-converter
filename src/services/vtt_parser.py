import re


def clean_vtt_content(content: str) -> list[str]:
    """
    Cleans the VTT content by removing headers, timestamps, and tags from text lines,
    and returns a list of unique, cleaned text lines.
    """
    lines = content.splitlines()
    cleaned_lines: list[str] = []
    unique_lines: set[str] = set()

    # Skip header (until the first blank line)
    try:
        header_end_index = lines.index("")
        lines = lines[header_end_index + 1 :]
    except ValueError:
        # No blank line found, assume no header or content
        return []

    for line in lines:
        # Skip empty lines and timestamps
        if not line.strip() or "-->" in line:
            continue

        # Clean the line by removing all tags
        cleaned_line = re.sub(r"<[^>]+>", "", line).strip()

        if cleaned_line and cleaned_line not in unique_lines:
            unique_lines.add(cleaned_line)
            cleaned_lines.append(cleaned_line)

    return cleaned_lines


def parse_vtt_file(file_path: str) -> list[str]:
    """
    Parses a VTT file, cleans its content, and returns unique text lines.
    """
    with open(file_path, encoding="utf-8") as f:
        content = f.read()
    return clean_vtt_content(content)
