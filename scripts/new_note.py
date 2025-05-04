import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv


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


def write_obfuscated_copy(note_path: Path):
    content = note_path.read_text(encoding="utf-8")
    obfuscated = obfuscate(content, get_sensitive_map())

    parts = note_path.parts
    if "notes" not in parts:
        print("❌ File is not under notes/ directory")
        return

    idx = parts.index("notes")
    obf_path = Path("obfuscated").joinpath(*parts[idx + 1 :])
    obf_path.parent.mkdir(parents=True, exist_ok=True)
    obf_path.write_text(obfuscated, encoding="utf-8")

    print(f"✅ Obfuscated note saved to {obf_path}")


load_dotenv()

now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
time_str = now.strftime("%H-%M-%S")

# Temporary placeholder file
temp_file = Path("__temp_note__.md")
temp_file.touch()

# Open the editor to let the user write
if shutil.which("code"):
    subprocess.run(["code", "--wait", str(temp_file)])
elif shutil.which("pycharm"):
    subprocess.run(["pycharm", str(temp_file)])
elif shutil.which("nano"):
    subprocess.run(["nano", str(temp_file)])
else:
    print(f"⚠️ Could not find a known editor. Note created at {temp_file}")

# After editing, check for datetime header
first_line = (
    temp_file.read_text(encoding="utf-8").splitlines()[0] if temp_file.exists() else ""
)
dt_match = re.match(r"^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})", first_line)
if dt_match:
    date_str = dt_match.group(1)
    time_str = dt_match.group(2).replace(":", "-")

notes_dir = Path("notes") / date_str
notes_dir.mkdir(parents=True, exist_ok=True)
file_path = notes_dir / f"{time_str}.md"
file_contents = temp_file.read_text(encoding="utf-8").splitlines()
if dt_match:
    file_contents = file_contents[1:]  # remove datetime header if present
file_path.write_text("".join(file_contents), encoding="utf-8")
temp_file.unlink()

# Start watchexec for obfuscation on save
script_path = Path(__file__).resolve()
from time import sleep

# Wait briefly to allow editor to fully release file handles
sleep(1)
write_obfuscated_copy(file_path)

print(f"✅ Note created at {file_path} and obfuscation watcher started")
sys.exit(0)
