import hashlib
import os
from dotenv import load_dotenv

ENV_PATH = ".env"

load_dotenv(ENV_PATH)

def obfuscate_token(term: str, category: str) -> str:
    short_hash = hashlib.sha256(term.lower().encode()).hexdigest()[:4]
    return f"\U0001f510{category.upper()}_{short_hash}\U0001f510"

def normalize_key(term: str) -> str:
    return term.strip().replace(" ", "_")

def add_entry(term: str, category: str):
    key = f"SENSITIVE_{normalize_key(term)}"
    value = obfuscate_token(term, category)

    # Check if it already exists
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if line.strip().startswith(f"{key}="):
                print(f"⚠️  Entry for '{term}' already exists in .env")
                return
            if line.strip().endswith(f"={value}"):
                print(f"⚠️  Obfuscated token '{value}' already exists in .env — possible collision?")
                return

    # Append to .env
    with open(ENV_PATH, "a", encoding="utf-8") as f:
        f.write(f"{key}={value}\n")
    print(f"✅ Added: {key}={value}")

if __name__ == "__main__":
    print("Add a new obfuscation mapping to your .env")
    term = input("Enter sensitive term (e.g. Apple, Project Zeus): ").strip()
    category = input("Enter category (e.g. company, project, person): ").strip()

    if not term or not category:
        print("❌ Term and category must not be empty.")
    else:
        add_entry(term, category)