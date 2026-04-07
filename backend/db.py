"""
Local ChromaDB vector store for offline medical protocols.
Seeded once on startup; all queries run fully offline.
"""

import chromadb
from chromadb.utils import embedding_functions
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.protocols import PROTOCOLS

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
COLLECTION_NAME = "medical_protocols"

_client = None
_collection = None


def _get_collection():
    global _client, _collection
    if _collection is not None:
        return _collection

    ef = embedding_functions.DefaultEmbeddingFunction()
    _client = chromadb.PersistentClient(path=DB_PATH)

    existing = [c.name for c in _client.list_collections()]
    if COLLECTION_NAME in existing:
        _collection = _client.get_collection(
            name=COLLECTION_NAME, embedding_function=ef
        )
    else:
        _collection = _client.create_collection(
            name=COLLECTION_NAME, embedding_function=ef
        )
        _collection.add(
            ids=[p["id"] for p in PROTOCOLS],
            documents=[p["content"] for p in PROTOCOLS],
            metadatas=[{"title": p["title"], "category": p["category"]} for p in PROTOCOLS],
        )
        print(f"[DB] Seeded {len(PROTOCOLS)} protocols into ChromaDB.")

    return _collection


def query_protocols(query: str, n_results: int = 3) -> list[dict]:
    """Return the top-n most relevant protocol chunks for a given query."""
    col = _get_collection()
    results = col.query(query_texts=[query], n_results=n_results)

    protocols = []
    for i, doc in enumerate(results["documents"][0]):
        protocols.append(
            {
                "title": results["metadatas"][0][i]["title"],
                "category": results["metadatas"][0][i]["category"],
                "content": doc,
            }
        )
    return protocols
