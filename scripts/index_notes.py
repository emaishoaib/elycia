from pathlib import Path

from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.storage.storage_context import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

load_dotenv()

# Read markdown files from obfuscated/
docs = []
for md_file in Path("obfuscated").rglob("*.md"):
    content = md_file.read_text(encoding="utf-8").strip()
    if content:
        # Extract metadata
        parts = md_file.parts
        if "obfuscated" in parts:
            idx = parts.index("obfuscated")
            try:
                date_str = parts[idx + 1]
                time_str = md_file.stem  # filename without .md
                metadata = {
                    "filename": md_file.name,
                    "date": date_str,
                    "time": time_str,
                }
                docs.append(Document(text=content, metadata=metadata))
            except IndexError:
                print(f"⚠️ Could not extract date/time from {md_file}")

if not docs:
    print("⚠️ No documents found in obfuscated/. Nothing to index.")
    exit()

# Correct Chroma client setup (v0.5.17+)
chroma_client = chromadb.PersistentClient(path="./brain")

chroma_collection = chroma_client.create_collection("elycia")

# Chroma + LlamaIndex integration
chroma_store = ChromaVectorStore(chroma_collection=chroma_collection, client=chroma_client)
storage_context = StorageContext.from_defaults(vector_store=chroma_store)

index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)
index.storage_context.persist()

print(f"✅ Indexed {len(docs)} obfuscated note file(s) into ./brain")