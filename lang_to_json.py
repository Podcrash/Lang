#!/usr/bin/env python3
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

def parse_lang_file(path: Path) -> dict:
    """Parse a .lang file into a key/value dict."""
    data = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        # Keep raw line endings out, strip just newline characters
        if not line or line.lstrip().startswith("#"):
            # Skip empty lines and comments for JSON structure
            continue

        # Only split on the first '='
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        data[key] = value
    return data

def convert_dir(lang_dir: Path):
    """Convert one pack directory with .lang files into its sibling *-json directory."""
    if not lang_dir.is_dir():
        return
    if lang_dir.name.endswith("-json"):
        # Skip JSON dirs, those are the targets
        return

    lang_files = sorted(lang_dir.glob("*.lang"))
    if not lang_files:
        # No .lang files here, nothing to do
        return

    json_dir_name = f"{lang_dir.name}-json"
    json_dir = BASE_DIR / json_dir_name
    json_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== Converting {lang_dir} -> {json_dir} ===")

    for lang_file in lang_files:
        locale = lang_file.stem  # e.g. en_US
        data = parse_lang_file(lang_file)
        if not data:
            print(f"⚠ {lang_file} has no key=value entries, skipping")
            continue

        json_path = json_dir / f"{locale}.json"
        with json_path.open("w", encoding="utf-8") as f:
            # Sorted for stable diffs; remove sorted() if you prefer source order
            ordered = {k: data[k] for k in sorted(data.keys())}
            json.dump(ordered, f, ensure_ascii=False, indent=2)

        print(f"✔ {json_path} ({len(data)} entries)")

def main():
    # Look at each immediate subdirectory of the repo root
    for subdir in sorted(BASE_DIR.iterdir()):
        if subdir.is_dir():
            convert_dir(subdir)

if __name__ == "__main__":
    main()
