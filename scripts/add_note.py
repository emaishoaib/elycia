import os
from datetime import datetime
from obfuscate import get_sensitive_map, obfuscate

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