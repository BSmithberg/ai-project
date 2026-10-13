import os
from dotenv import load_dotenv

load_dotenv()

import chromadb
from sentence_transformers import SentenceTransformer

from .load_docs import load_documents
from .chunk_docs import simple_chunk

EMBED_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2"
)

model = SentenceTransformer(EMBED_MODEL)


def embed_texts(texts):
    """
    Generate embeddings using Sentence Transformers.
    """
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return embeddings.tolist()


def build_vector_store():
    client = chromadb.PersistentClient(path="data/chroma")

    collection = client.get_or_create_collection(
        name="policies",
        metadata={"hnsw:space": "cosine"}
    )

    docs = load_documents()

    ids = []
    texts = []
    metadatas = []

    for doc in docs:
        chunks = simple_chunk(doc["text"])

        for i, chunk in enumerate(chunks):
            ids.append(f"{doc['id']}_{i}")
            texts.append(chunk)
            metadatas.append({
                "source": doc["id"],
                "chunk_id": i
            })

    embeddings = embed_texts(texts)

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print("Vector store built successfully.")


if __name__ == "__main__":
    build_vector_store()

