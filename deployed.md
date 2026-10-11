# Deployment

## Hosting choice

- **Platform:** Render (or Railway)
- **Runtime:** Python 3.11
- **Process type:** `web`

## Repository structure

Key files:

- `app.py`
- `requirements.txt`
- `ingestion/` (ingestion pipeline)
- `rag/` (RAG pipeline)
- `eval/` (evaluation scripts)
- `data/` (policy documents and Chroma store)

## Deployment steps (Render example)

1. **Create service:**
   - New Web Service → connect GitHub repo.
2. **Environment:**
   - Set runtime to Python.
3. **Build command:**
   - `pip install -r requirements.txt`
4. **Start command:**
   - `python app.py`
5. **Environment variables:**
   - `GROQ_API_KEY=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`
   - `VOYAGE_API_KEY=pa-96ldveRZkEXgcIRZUt8sKi5n88rk8W4ZVKepbPiw12L`
   - `LLM_MODEL=llama-3.1-70b-versatile`
   - `EMBEDDING_MODEL=voyage-3`
6. **Data:**
   - Upload policy documents to `data/policies_raw/` in the repo.
   - Run ingestion locally (`python ingestion/embed_store.py`) and commit `data/chroma/` if desired, or run ingestion on the server via a one‑off job.

## Public URL

- **App URL:** `https://<your-service-name>.onrender.com/`
  - `/` — web UI
  - `/chat` — POST endpoint (JSON)
  - `/health` — health check

## Smoke test

- Visit `/health` → expect `{"status": "ok"}`.
- Visit `/` → ask a policy question and verify answer + citations.
