import json
import os
from rag.generation import answer_query

QUESTIONS_PATH = "eval/questions.json"
OUTPUT_PATH = "eval/results.json"

def load_questions():
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def evaluate():
    questions = load_questions()
    results = []

    for q in questions:
        print(f"Evaluating Q{q['id']}: {q['question']}")
        result = answer_query(q["question"])

        # Prepare evaluator-friendly record
        record = {
            "id": q["id"],
            "topic": q["topic"],
            "question": q["question"],
            "answer": result["answer"],
            "citations": result["citations"],
            "snippets": result["snippets"],

            # Fields the evaluator will fill in manually
            "groundedness_score": null,        # 0–1 scale
            "citation_accuracy_score": null    # 0–1 scale
        }

        results.append(record)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nEvaluation complete. Results saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    evaluate()
