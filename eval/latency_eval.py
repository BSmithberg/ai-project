import json
import time
from rag.generation import answer_query

QUESTIONS_PATH = "eval/questions.json"

def load_questions():
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def measure_latency():
    questions = load_questions()
    latencies = []

    for q in questions:
        start = time.time()
        _ = answer_query(q["question"])
        elapsed = time.time() - start
        latencies.append(elapsed)
        print(f"Q{q['id']} latency: {elapsed:.3f}s")

    latencies.sort()
    n = len(latencies)

    p50 = latencies[int(0.50 * n)]
    p95 = latencies[int(0.95 * n)]

    print("\nLatency Summary:")
    print(f"p50: {p50:.3f}s")
    print(f"p95: {p95:.3f}s")

if __name__ == "__main__":
    measure_latency()
