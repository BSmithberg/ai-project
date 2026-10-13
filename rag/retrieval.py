import os
from dotenv import load_dotenv

load_dotenv()

import chromadb
from sentence_transformers import SentenceTransformer

EMBED_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2"
)

model = SentenceTransformer(EMBED_MODEL)

client = chromadb.PersistentClient(path="data/chroma")
collection = client.get_collection("policies")


def embed_query(query: str):
    embedding = model.encode(query)
    return embedding.tolist()


def retrieve(query: str, k: int = 3):
    query_embedding = embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    chunks = []

    for text, meta in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        chunks.append({
            "text": text,
            "meta": meta
        })

    return chunks

