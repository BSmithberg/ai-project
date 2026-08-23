import os
from dotenv import load_dotenv
load_dotenv()

import requests
from rag.retrieval import retrieve
from rag.guardrails import is_in_scope, format_context, refusal_message, sanitize

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "mixtral-8x7b-32768")

def call_llm(prompt):
    url = "https://api.groq.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def answer_query(query: str):
    if not is_in_scope(query):
        return {"answer": refusal_message(), "citations": []}

    chunks = retrieve(query, k=3)
    context = format_context(chunks)

    prompt = (
        "You are a company policy assistant.\n"
        "Answer ONLY using the context provided.\n"
        "If the answer is not in the context, say so.\n\n"
        "CONTEXT (each item includes SOURCE + CHUNK ID):\n"
        f"{context}\n\n"
        "QUESTION:\n"
        f"{query}\n\n"
        "INSTRUCTIONS:\n"
        "- Use only information from the context.\n"
        "- Cite sources using: (SOURCE: X, CHUNK: Y).\n"
        "- Keep the answer concise.\n\n"
        "ANSWER:\n"
    )

    answer = call_llm(prompt)
    citations = list({c["meta"]["source"] for c in chunks})

    return {
        "answer": answer,
        "citations": citations,
        "snippets": chunks
    }
