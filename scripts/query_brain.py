import os

from dotenv import load_dotenv
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.vector_stores.chroma import ChromaVectorStore
from pathlib import Path
import chromadb
import shutil
import subprocess

load_dotenv()

# Build reverse map from .env
reverse_map = {}
for key, value in os.environ.items():
    if key.startswith("SENSITIVE_"):
        reverse_map[value] = key.removeprefix("SENSITIVE_").replace("_", " ")

chroma_client = chromadb.PersistentClient(path="./brain")
chroma_collection = chroma_client.get_or_create_collection("elycia")
chroma_store = ChromaVectorStore(
    chroma_collection=chroma_collection, client=chroma_client
)
storage_context = StorageContext.from_defaults(
    vector_store=chroma_store, persist_dir="./brain"
)
index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()

while True:
    query = input("🔍 Ask your brain something (or 'exit'): ").strip()
    if query.lower() in {"exit", "quit"}:
        break

    response = query_engine.query(query)
    output = str(response)
    for obfuscated, original in reverse_map.items():
        output = output.replace(obfuscated, original)

    # Create temporary markdown preview file
    preview_file = Path("__query_preview__.md")
    preview_file.write_text(f"# ❓ {query}\n\n{output}", encoding="utf-8")

    # Open in available editor
    if shutil.which("code"):
        subprocess.run(["code", "--wait", str(preview_file)])
    elif shutil.which("pycharm"):
        subprocess.run(["pycharm", str(preview_file)])
    elif shutil.which("nano"):
        subprocess.run(["nano", str(preview_file)])
    else:
        print(f"📄 Result:\n\n{str(response)}")

    preview_file.unlink(missing_ok=True)
    print("\n" + "=" * 60 + "\n")
