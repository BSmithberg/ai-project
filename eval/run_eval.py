import json
import time
import statistics
import numpy as np

from rag.generation import answer_query

QUESTIONS_PATH = "eval/questions.json"
OUTPUT_PATH = "eval/results.json"


def load_questions():
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate():

    questions = load_questions()

    results = []
    latencies = []

    citation_scores = []
    groundedness_scores = []

    for q in questions:

        print(f"Evaluating Q{q['id']}: {q['question']}")

        start_time = time.perf_counter()

        result = answer_query(q["question"])

        latency = time.perf_counter() - start_time

        latencies.append(latency)

        citations = result.get("citations", [])
        snippets = result.get("snippets", [])

        citation_score = 1.0 if citations else 0.0

        groundedness_score = min(
            len(snippets) / 3,
            1.0
        )

        citation_scores.append(citation_score)
        groundedness_scores.append(groundedness_score)

        record = {
            "id": q["id"],
            "topic": q["topic"],
            "question": q["question"],

            "answer": result.get("answer", ""),

            "citations": citations,

            "snippets": snippets,

            "latency_seconds": round(latency, 3),

            "citation_accuracy_score": round(
                citation_score,
                2
            ),

            "groundedness_score": round(
                groundedness_score,
                2
            )
        }

        results.append(record)

    summary = {
        "questions_evaluated": len(results),

        "average_latency_seconds": round(
            statistics.mean(latencies),
            3
        ),

        "p50_latency_seconds": round(
            float(np.percentile(latencies, 50)),
            3
        ),

        "p95_latency_seconds": round(
            float(np.percentile(latencies, 95)),
            3
        ),

        "average_citation_score": round(
            statistics.mean(citation_scores),
            2
        ),

        "average_groundedness_score": round(
            statistics.mean(groundedness_scores),
            2
        )
    }

    output = {
        "summary": summary,
        "results": results
    }

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            output,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("\nEvaluation Complete")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    evaluate()