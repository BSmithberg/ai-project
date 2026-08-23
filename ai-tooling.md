# AI tooling usage

## Overview

This project intentionally uses AI tooling to accelerate development while maintaining human control over architecture, correctness, and evaluation.

## Where AI was used

- **Code scaffolding:**
  - Initial structure for `ingestion/`, `rag/`, and `eval/` packages.
  - Drafts of `app.py` and basic Flask routing.
- **RAG pipeline design:**
  - Suggestions for chunking strategy, top‑k retrieval, and prompt structure.
- **Provider integration:**
  - Template code for Groq chat completions and VoyageAI embeddings.

## Where human judgment was critical

- **Architecture decisions:**
  - Choosing Groq + VoyageAI for speed and quality.
  - Selecting Chroma as the vector store for simplicity and reproducibility.
- **Policy alignment:**
  - Ensuring prompts and guardrails reflect the intended “company policy assistant” behavior.
- **Evaluation design:**
  - Defining groundedness and citation accuracy criteria.
  - Curating questions in `eval/questions.json` to match the policy domain.

## Validation and refinement

- **Manual review:**
  - Verified imports, package structure, and environment variables.
  - Confirmed that `answer_query()` returns answers with citations and snippets.
- **Testing:**
  - Ran ingestion (`embed_store.py`) to build the vector store.
  - Tested end‑to‑end via `test_llm_and_embeddings.py` and the Flask `/chat` endpoint.
  - Measured latency and inspected `eval/results.json` for answer quality.

## Conclusion

AI tooling accelerated boilerplate and integration work, but core design, evaluation, and final validation were guided by human judgment to ensure the system meets the project requirements and behaves reliably.
