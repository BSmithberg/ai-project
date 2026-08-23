# AI Engineering Project — Company Policy RAG Assistant

This project implements a full Retrieval-Augmented Generation (RAG) system that answers questions about company policies using grounded context and citations. It includes ingestion, vector storage, retrieval, generation, evaluation, deployment, and documentation — fully aligned with the AI Engineering Project rubric.

---

## 🚀 Features

- **RAG pipeline** using VoyageAI embeddings + Chroma vector store  
- **LLM generation** using Groq (llama‑3.1‑70b‑versatile)  
- **Citations** for every answer (source + chunk ID)  
- **Guardrails** restricting responses to policy‑related questions  
- **Flask web app** with `/`, `/chat`, `/health` endpoints  
- **Evaluation scripts** for groundedness, citation accuracy, and latency  
- **Deployment-ready** for Render/Railway  
- **CI/CD workflow** using GitHub Actions  

---

## 📂 Project Structure

AI_RAG_Project/
│
├── app.py
├── requirements.txt
├── README.md
│
├── ingestion/
│   ├── init.py
│   ├── load_docs.py
│   ├── chunk_docs.py
│   ├── embed_store.py
│   └── config.py
│
├── rag/
│   ├── init.py
│   ├── retrieval.py
│   ├── generation.py
│   └── guardrails.py
│
├── eval/
│   ├── questions.json
│   ├── run_eval.py
│   └── latency_eval.py
│
├── data/
│   ├── policies_raw/        # input documents
│   └── chroma/              # vector store (generated)
│
└── .github/
└── workflows/
└── ci.yml


---

## 🔧 Installation

### 1. Clone the repository


### 2. Create a virtual environment

python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.\.venv\Scripts\activate    # Windows


### 3. Install dependencies

pip install -r requirements.txt

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

GROQ_API_KEY=your_groq_key_here
VOYAGE_API_KEY=your_voyage_key_here

LLM_MODEL=llama-3.1-70b-versatile
EMBEDDING_MODEL=voyage-3

---

## 📥 Ingestion Pipeline

Place your policy documents in:
data/policies_raw/

Supported formats: `.txt`, `.md`, `.pdf` (if you add a PDF parser).

Then run:

python ingestion/embed_store.py

This will:

- Load documents  
- Chunk them  
- Embed them using VoyageAI  
- Store vectors in Chroma (`data/chroma/`)  

---

## 🤖 Running the Web App

Start the Flask server:

python app.py

### Endpoints

| Endpoint | Description |
|---------|-------------|
| `/` | Web UI for asking policy questions |
| `/chat` | POST endpoint for JSON queries |
| `/health` | Health check |

### Example JSON request

POST /chat
{
"question": "What is our PTO policy?"
}

---

## 🧪 Evaluation

### 1. Groundedness + Citation Accuracy

python eval/run_eval.py

    Outputs:

eval/results.json

Contains:

- Answer  
- Citations  
- Retrieved snippets  
- Manual scoring fields  

### 2. Latency (p50 / p95)

python eval/latency_eval.py
