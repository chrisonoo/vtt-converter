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


if __name__ == "__main__":
    # Example usage with the provided VTT snippet
    vtt_snippet = """WEBVTT
Kind: captions
Language: pl

00:05:14.440 --> 00:05:17.230 align:start position:0%

Cześć.<00:05:15.080><c> Witam</c><00:05:15.400><c> was</c><00:05:15.600><c> wszystkich</c><00:05:16.120><c> na</c><00:05:16.880><c> drugiej</c>

00:05:17.230 --> 00:05:17.240 align:start position:0%
Cześć. Witam was wszystkich na drugiej


00:0s:17.240 --> 00:05:21.550 align:start position:0%
Cześć. Witam was wszystkich na drugiej
emisji<00:05:17.800><c> online</c><00:05:18.639><c> umiejętności</c><00:05:19.240><c> jutra</c><00:05:19.919><c> AI20.0.</c>

00:05:21.550 --> 00:05:21.560 align:start position:0%
emisji online umiejętności jutra AI20.0.


00:05:21.560 --> 00:05:24.629 align:start position:0%
emisji online umiejętności jutra AI20.0.
Cieszę<00:05:21.960><c> się,</c><00:05:22.240><c> że</c><00:05:22.400><c> jesteśmy</c><00:05:23.160><c> tak</c><00:05:23.400><c> liczni.</c><00:05:24.479><c> Na</c>

00:05:24.629 --> 00:05:24.639 align:start position:0%
Cieszę się, że jesteśmy tak liczni. Na


00:05:24.639 --> 00:05:27.350 align:start position:0%
Cieszę się, że jesteśmy tak liczni. Na
platformie<00:05:25.199><c> jest</c><00:05:25.400><c> nas</c><00:05:25.560><c> już</c><00:05:25.919><c> 40</c><00:05:26.680><c> 000</c>

00:05:27.350 --> 00:05:27.360 align:start position:0%
platformie jest nas już 40 000


00:05:27.360 --> 00:05:29.110 align:start position:0%
platformie jest nas już 40 000
użytkowników.

00:05:29.110 --> 00:05:29.120 align:start position:0%
użytkowników.


00:05:29.120 --> 00:05:31.790 align:start position:0%
użytkowników.
Rozpoczęliśmy<00:05:30.120><c> drugi</c><00:05:30.440><c> tydzień</c><00:05:30.800><c> nauki.</c><00:05:31.600><c> W</c>

00:05:31.790 --> 00:05:31.800 align:start position:0%
Rozpoczęliśmy drugi tydzień nauki. W


00:05:31.800 --> 00:05:34.710 align:start position:0%
Rozpoczęliśmy drugi tydzień nauki. W
pierwszym<00:05:32.160><c> tygodniu</c><00:05:33.160><c> pokryliśmy</c><00:05:34.000><c> podstawy</c>

00:05:34.710 --> 00:05:34.720 align:start position:0%
pierwszym tygodniu pokryliśmy podstawy


00:05:34.720 --> 00:05:37.749 align:start position:0%
pierwszym tygodniu pokryliśmy podstawy
generatywnej<00:05:36.080><c> sztucznej</c><00:05:36.479><c> inteligencji.</c><00:05:37.600><c> W</c>

00:05:37.749 --> 00:05:37.759 align:start position:0%
generatywnej sztucznej inteligencji. W
"""
    cleaned_text = clean_vtt_content(vtt_snippet)
    for text in cleaned_text:
        print(text)

    # Expected output should be the same, but now the logic is robust
    # Cześć. Witam was wszystkich na drugiej
    # emisji online umiejętności jutra AI20.0.
    # Cieszę się, że jesteśmy tak liczni. Na
    # platformie jest nas już 40 000
    # użytkowników.
    # Rozpoczęliśmy drugi tydzień nauki. W
    # pierwszym tygodniu pokryliśmy podstawy
    # generatywnej sztucznej inteligencji. W
