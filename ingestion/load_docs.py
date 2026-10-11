import os
from pathlib import Path

def load_documents(root: str = "data/policies_raw"):
    docs = []
    for path in Path(root).rglob("*"):
        if path.suffix.lower() in {".md", ".txt", ".html"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            docs.append({"id": str(path), "text": text})
        # PDFs: you can add pdfplumber or pypdf here if needed
    return docs
