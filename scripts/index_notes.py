from pathlib import Path
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.storage.storage_context import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

# Read markdown files from obfuscated/
docs = []
for md_file in Path("obfuscated").glob("*.md"):
    content = md_file.read_text(encoding="utf-8").strip()
    if content:
        docs.append(Document(text=content, metadata={"filename": md_file.name}))

if not docs:
    print("⚠️ No documents found in obfuscated/. Nothing to index.")
    exit()

# Correct Chroma client setup (v0.5.17+)
chroma_client = chromadb.PersistentClient(path="./brain")

# Chroma + LlamaIndex integration
chroma_store = ChromaVectorStore(chroma_collection="second_brain", client=chroma_client)
storage_context = StorageContext.from_defaults(vector_store=chroma_store)

index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)
index.storage_context.persist()

print(f"✅ Indexed {len(docs)} obfuscated note file(s) into ./brain")