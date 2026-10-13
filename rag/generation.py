import os
import requests

from dotenv import load_dotenv

from rag.retrieval import retrieve
from rag.guardrails import (
    is_in_scope,
    format_context,
    refusal_message,
    sanitize
)

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3-8b-8192")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def call_llm(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1
    }

    response = requests.post(
        GROQ_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]


def answer_query(query: str):
    """
    Main RAG pipeline:
      1. Check scope
      2. Retrieve chunks
      3. Build context
      4. Generate answer
      5. Return answer + citations + snippets
    """

    if not is_in_scope(query):
        return {
            "answer": refusal_message(),
            "citations": [],
            "snippets": []
        }

    chunks = retrieve(query, k=3)

    if not chunks:
        return {
            "answer": "No relevant information was found in the policy documents.",
            "citations": [],
            "snippets": []
        }

    context = format_context(chunks)

    prompt = f"""
You are a company policy assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context, explicitly say:

"The answer is not available in the provided policy documents."

CONTEXT:
{context}

QUESTION:
{query}

INSTRUCTIONS:
- Use only facts from the context.
- Do not invent information.
- Keep the response concise.
- Include source references when possible.
- Cite using the format:
  (SOURCE: source_name, CHUNK: chunk_id)

ANSWER:
"""

    try:
        answer = call_llm(prompt)

    except Exception as ex:
        return {
            "answer": f"LLM error: {str(ex)}",
            "citations": [],
            "snippets": chunks
        }

    citations = sorted(
        list(
            {
                chunk["meta"]["source"]
                for chunk in chunks
                if "source" in chunk["meta"]
            }
        )
    )

    return {
        "answer": sanitize(answer),
        "citations": citations,
        "snippets": chunks
    }