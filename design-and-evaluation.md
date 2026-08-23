# Design and evaluation

## System overview

**Goal:** A RAG-based company policy assistant that answers questions grounded in internal policy documents, with citations.

**Core components:**

- **Ingestion:** Load, chunk, embed documents and store them in Chroma.
- **Retrieval:** Top‑k semantic search over embedded chunks.
- **Generation:** Groq LLM (llama‑3.1‑70b‑versatile) constrained by retrieved context.
- **Evaluation:** Groundedness, citation accuracy, and latency (p50/p95).

## Architecture

- **Backend:** Python + Flask (`app.py`)
- **Vector store:** Chroma (DuckDB + Parquet, cosine space)
- **Embeddings:** VoyageAI (`voyage-3`)
- **LLM:** Groq (`llama-3.1-70b-versatile`)
- **Packages:**
  - `ingestion/` — `load_docs.py`, `chunk_docs.py`, `embed_store.py`
  - `rag/` — `retrieval.py`, `guardrails.py`, `generation.py`
  - `eval/` — `questions.json`, `run_eval.py`, `latency_eval.py`

## RAG design decisions

### Document ingestion

- **Sources:** Files under `data/policies_raw/` (e.g., `.md`, `.txt`, `.pdf` via parser).
- **Chunking:**
  - Approximate token‑based chunking using word counts.
  - Max chunk size ≈ 512 words, overlap ≈ 64 words.
  - Rationale: balance between enough context and avoiding prompt bloat.

### Embeddings and vector store

- **Embedding model:** VoyageAI `voyage-3`.
- **Store:** Chroma collection `policies` with cosine similarity.
- **Metadata:** `source` (file path) and `chunk_id` per chunk for citation tracking.

### Retrieval

- **Top‑k:** `k = 5` chunks per query.
- **Query:** Chroma semantic query using the user’s question.
- **Returned data:** `id`, `text`, `meta` (source, chunk_id).

### Generation and guardrails

- **LLM:** Groq chat completions API, `llama-3.1-70b-versatile`, `temperature=0.0`.
- **Prompt:**
  - System: “You are a company policy assistant. Answer ONLY using the provided context.”
  - User: Context + question + instruction to cite SOURCE and CHUNK IDs.
- **Guardrails:**
  - `is_in_scope(query)` placeholder for policy‑domain filtering.
  - If out of scope → refusal message: “I can only answer questions about our company policies and procedures.”
- **Citations:**
  - Derived from `meta["source"]` of retrieved chunks.
  - Displayed alongside the answer.

## Evaluation

### Groundedness and citation accuracy

- **Data:** `eval/questions.json` — curated policy questions.
- **Process (`run_eval.py`):**
  - For each question:
    - Call `answer_query()`.
    - Save `answer`, `citations`, and `snippets` to `eval/results.json`.
    - Include `groundedness_score` and `citation_accuracy_score` fields for manual scoring (0–1).
- **Interpretation:**
  - **Groundedness:** How strictly the answer stays within provided context.
  - **Citation accuracy:** Whether cited sources actually support the answer.

### Latency

- **Process (`latency_eval.py`):**
  - For each question:
    - Measure total time for `answer_query()`.
  - Compute:
    - `p50` (median latency).
    - `p95` (95th percentile latency).
- **Factors:**
  - VoyageAI embedding retrieval (pre‑computed).
  - Chroma query time.
  - Groq LLM response time.

## Summary

This design provides:

- A clear, modular RAG pipeline.
- Strong embeddings (VoyageAI) and fast LLM (Groq).
- Explicit evaluation scripts for groundedness, citation accuracy, and latency.
- A structure that is easy to extend (re‑ranking, better guardrails, more questions) if needed.
