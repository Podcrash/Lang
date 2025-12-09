#!/usr/bin/env python3
import json
from pathlib import Path

SOURCE_DIR = Path("FARMING")          # folder with .lang
TARGET_DIR = Path("FARMING-json")     # folder for .json
TARGET_DIR.mkdir(exist_ok=True)

def parse_lang_file(path: Path) -> dict:
    data = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.lstrip().startswith("#"):
                # skip empty lines and comments in JSON – structure only
                continue
            # split on first '=' ONLY
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            data[key] = value
    return data

def main():
    for lang_file in SOURCE_DIR.glob("*.lang"):
        locale = lang_file.stem  # e.g. en_US
        data = parse_lang_file(lang_file)
        out_path = TARGET_DIR / f"{locale}.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Written {out_path} ({len(data)} entries)")

if __name__ == "__main__":
    main()
