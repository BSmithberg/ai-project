import os
from dotenv import load_dotenv
load_dotenv()

import chromadb
import voyageai

EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "voyage-large-2")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")

voyage = voyageai.Client(api_key=VOYAGE_API_KEY)

client = chromadb.PersistentClient(path="data/chroma")
collection = client.get_collection("policies")

def embed_query(query: str):
    response = voyage.embed([query], model=EMBED_MODEL)
    return response.embeddings[0]

def retrieve(query: str, k: int = 3):
    query_embedding = embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    chunks = []
    for text, meta in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append({
            "text": text,
            "meta": meta
        })

    return chunks

