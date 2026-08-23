from rag.generation import answer_query

print("Testing Groq + VoyageAI RAG pipeline...\n")

result = answer_query("What is our PTO policy?")
print(result)
