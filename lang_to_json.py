#!/usr/bin/env python3
import json
from pathlib import Path

SOURCE_DIR = Path("FARMING")
TARGET_DIR = Path("FARMING-json")
TARGET_DIR.mkdir(exist_ok=True)

def parse_lang(path: Path):
    data = {}
    for line in path.read_text(encoding="utf8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key] = value
    return data

for langfile in SOURCE_DIR.glob("*.lang"):
    locale = langfile.stem
    data = parse_lang(langfile)
    out = TARGET_DIR / f"{locale}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf8")
    print("Converted", langfile, "→", out)
