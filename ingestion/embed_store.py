import os
from dotenv import load_dotenv
load_dotenv()
import chromadb
from .load_docs import load_documents
from .chunk_docs import simple_chunk
import voyageai

# Initialize Voyage client
voyage = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "voyage-large-2")

def embed_texts(texts):
    """
    Returns list of embeddings for a list of texts.
    VoyageAI automatically handles batching.
    """
    response = voyage.embed(texts, model=EMBED_MODEL)
    return response.embeddings

def build_vector_store():
    # NEW Chroma client (persistent)
    client = chromadb.PersistentClient(path="data/chroma")

    # Create or load collection
    collection = client.get_or_create_collection(
        name="policies",
        metadata={"hnsw:space": "cosine"}
    )

    docs = load_documents()
    ids, texts, metadatas = [], [], []

    for doc in docs:
        text = doc["text"]
        chunks = simple_chunk(text)

        for i, chunk in enumerate(chunks):
            ids.append(f"{doc['id']}_{i}")
            texts.append(chunk)
            metadatas.append({"source": doc["id"], "chunk_id": i})

    # Embed all chunks
    embeddings = embed_texts(texts)

    # Add to Chroma
    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print("Vector store built successfully.")

if __name__ == "__main__":
    build_vector_store()
