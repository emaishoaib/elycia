import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# --- Obfuscation Mode ---
if len(sys.argv) == 3 and sys.argv[1] == "--obfuscate":
    load_dotenv()

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

    def write_obfuscated_copy(note_path: Path):
        content = note_path.read_text(encoding="utf-8")
        obfuscated = obfuscate(content, get_sensitive_map())

        parts = note_path.parts
        if "notes" not in parts:
            print("❌ File is not under notes/ directory")
            return

        idx = parts.index("notes")
        obf_path = Path("obfuscated").joinpath(*parts[idx + 1:])
        obf_path.parent.mkdir(parents=True, exist_ok=True)
        obf_path.write_text(obfuscated, encoding="utf-8")

        print(f"✅ Obfuscated note saved to {obf_path}")

    write_obfuscated_copy(Path(sys.argv[2]))
    sys.exit(0)

# --- Main Note-Taking Flow ---
load_dotenv()

now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
time_str = now.strftime("%H-%M-%S")

notes_dir = Path("notes") / date_str
notes_dir.mkdir(parents=True, exist_ok=True)
file_path = notes_dir / f"{time_str}.md"
file_path.touch()

if shutil.which("code"):
    subprocess.Popen(["code", str(file_path)])
elif shutil.which("pycharm"):
    subprocess.Popen(["pycharm", str(file_path)])
elif shutil.which("nano"):
    subprocess.run(["nano", str(file_path)])
else:
    print(f"⚠️ Could not find a known editor. Note created at {file_path}")

script_path = Path(__file__).resolve()
subprocess.Popen([
    "watchexec",
    "--restart",
    "--watch", str(file_path),
    "--exts", "md",
    "--", "poetry", "run", "python", str(script_path), "--obfuscate", str(file_path)
])

print(f"✅ Note opened and obfuscation watcher started: {file_path}")
sys.exit(0)
