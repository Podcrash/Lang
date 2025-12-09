#!/usr/bin/env python3
import json
from pathlib import Path

JSON_DIR = Path("FARMING-json")
LANG_DIR = Path("FARMING")

def convert_file(json_path: Path, lang_path: Path):
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Ensure output directory exists
    lang_path.parent.mkdir(parents=True, exist_ok=True)

    # Build .lang lines
    lines = []
    for key, value in data.items():
        # Preserve § codes and \n exactly as stored in JSON
        lines.append(f"{key}={value}")

    # Write .lang with correct line endings
    with lang_path.open("w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    print(f"✔ Wrote {lang_path} ({len(lines)} entries)")

def main():
    for json_file in JSON_DIR.glob("*.json"):
        locale = json_file.stem  # e.g. en_US
        out_file = LANG_DIR / f"{locale}.lang"
        convert_file(json_file, out_file)

if __name__ == "__main__":
    main()
