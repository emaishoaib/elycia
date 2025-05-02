import os
from datetime import datetime

def get_sensitive_map():
    return {
        key.replace("SENSITIVE_", ""): value
        for key, value in os.environ.items()
        if key.startswith("SENSITIVE_")
    }

def obfuscate(text: str, terms: dict) -> str:
    for term, token in terms.items():
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        text = pattern.sub(token, text)
    return text

def deobfuscate(text: str, terms: dict) -> str:
    reverse = {v: k for k, v in terms.items()}
    for token, term in reverse.items():
        text = text.replace(token, term)
    return text

raw_input = input("Paste your notes (semicolon-separated):\n")

notes = [note.strip() for note in raw_input.split(";") if note.strip()]
if not notes:
    print("⚠️ No valid notes found.")
    exit()

today = datetime.now().strftime("%Y-%m-%d.md")
raw_path = os.path.join("notes", today)
obf_path = os.path.join("obfuscated", today)

sensitive_terms = get_sensitive_map()

timestamp = datetime.now().strftime("%H:%M:%S")
header = f"\n### {timestamp}\n"

raw_block = header + "\n".join(f"- {n}" for n in notes)
obf_block = obfuscate(raw_block, sensitive_terms)

with open(raw_path, "a", encoding="utf-8") as f:
    f.write(raw_block + "\n")

with open(obf_path, "a", encoding="utf-8") as f:
    f.write(obf_block + "\n")

print(f"✅ Stored {len(notes)} note(s) to {today}")