from dotenv import load_dotenv
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.vector_stores.chroma import ChromaVectorStore
from chromadb import PersistentClient

load_dotenv()

chroma_client = PersistentClient(path="./brain")
chroma_collection = chroma_client.get_or_create_collection("elycia")
chroma_store = ChromaVectorStore(chroma_collection=chroma_collection, client=chroma_client)
storage_context = StorageContext.from_defaults(vector_store=chroma_store, persist_dir="./brain")
index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()

while True:
    query = input("🔍 Ask your brain something (or 'exit'): ").strip()
    if query.lower() in {"exit", "quit"}:
        break
    response = query_engine.query(query)
    print("\n📄 Result:\n")
    print(str(response))
    print("\n" + "="*60 + "\n")
