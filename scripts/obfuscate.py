import os
from dotenv import load_dotenv

load_dotenv()

def get_sensitive_map():
    return {
        key.replace("SENSITIVE_", ""): value
        for key, value in os.environ.items()
        if key.startswith("SENSITIVE_")
    }

def obfuscate(text: str, terms: dict) -> str:
    for term, token in terms.items():
        text = text.replace(term, token)
    return text

def deobfuscate(text: str, terms: dict) -> str:
    reverse = {v: k for k, v in terms.items()}
    for token, term in reverse.items():
        text = text.replace(token, term)
    return text