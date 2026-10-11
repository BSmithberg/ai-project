def simple_chunk(text: str, max_tokens: int = 512, overlap: int = 64):
    # token-free approximation: split by sentences/paragraphs, then group
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks = []
    current = []
    length = 0
    for p in paragraphs:
        l = len(p.split())
        if length + l > max_tokens:
            chunks.append(" ".join(current))
            current = p.split()[-overlap:]
            length = len(current)
        else:
            current.append(p)
            length += l
    if current:
        chunks.append(" ".join(current))
    return chunks
