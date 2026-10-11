from .embed_store import build_vector_store

def run_ingestion():
    print("🧠 Building vector store...")
    build_vector_store()
    print("✅ Ingestion complete!")

if __name__ == "__main__":
    run_ingestion()
