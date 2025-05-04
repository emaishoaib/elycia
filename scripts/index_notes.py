from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.storage.storage_context import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

load_dotenv()

# Load last indexed timestamp if available
INDEX_TIMESTAMP_FILE = Path(".last_indexed")
last_indexed = None
if INDEX_TIMESTAMP_FILE.exists():
    last_indexed = datetime.fromisoformat(INDEX_TIMESTAMP_FILE.read_text().strip())

# Read markdown files from obfuscated/
docs = []
for md_file in Path("obfuscated").rglob("*.md"):
    modified_time = datetime.fromtimestamp(md_file.stat().st_mtime)
    if last_indexed and modified_time <= last_indexed:
        continue

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
    print("⚠️ No new or modified documents to index.")
    exit()

chroma_client = chromadb.PersistentClient(path="./brain")
chroma_collection = chroma_client.get_or_create_collection("elycia")
chroma_store = ChromaVectorStore(
    chroma_collection=chroma_collection, client=chroma_client
)
storage_context = StorageContext.from_defaults(vector_store=chroma_store)

index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)
index.storage_context.persist(persist_dir="./brain")

# Update last indexed timestamp
INDEX_TIMESTAMP_FILE.write_text(datetime.now().isoformat())

print(f"✅ Indexed {len(index.docstore.docs)} new or modified note(s) into ./brain")
