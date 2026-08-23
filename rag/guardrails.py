import re

def is_in_scope(query: str) -> bool:
    q = query.lower()
    keywords = ["policy", "security", "access", "procedure", "guideline", "compliance"]
    return any(k in q for k in keywords)

def refusal_message() -> str:
    return "I can only answer questions about company policies based on the provided documents."

def sanitize(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)

    # Remove null bytes
    text = text.replace("\x00", "").replace("\u0000", "")

    # Remove invalid unicode surrogate pairs
    text = re.sub(r"[\ud800-\udfff]", "", text)

    # Remove non-printable characters
    text = re.sub(r"[^\x09\x0A\x0D\x20-\x7E]", " ", text)

    # Ensure valid UTF-8
    text = text.encode("utf-8", "replace").decode("utf-8")

    return text

def format_context(chunks):
    formatted = ""
    for c in chunks:
        clean_text = sanitize(c["text"])[:1200]  # hard cap per chunk
        formatted += (
            f"[SOURCE: {c['meta']['source']} | CHUNK: {c['meta']['chunk_id']}]\n"
            f"{clean_text}\n\n"
        )
    return formatted
