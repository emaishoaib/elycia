import os
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def get_sensitive_map():
    return {
        key.replace("SENSITIVE_", "").replace("_", " "): value
        for key, value in os.environ.items()
        if key.startswith("SENSITIVE_")
    }

def obfuscate(text: str, terms: dict) -> str:
    for term, token in terms.items():
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        text = pattern.sub(token, text)
    return text

def sync_notes():
    notes_root = Path("notes")
    obf_root = Path("obfuscated")
    terms = get_sensitive_map()

    for note_path in notes_root.rglob("*.md"):
        rel_path = note_path.relative_to(notes_root)
        obf_path = obf_root / rel_path
        content = note_path.read_text(encoding="utf-8")
        obfuscated = obfuscate(content, terms)

        obf_path.parent.mkdir(parents=True, exist_ok=True)
        obf_path.write_text(obfuscated, encoding="utf-8")
        print(f"✅ Synced: {rel_path}")

if __name__ == "__main__":
    sync_notes()
