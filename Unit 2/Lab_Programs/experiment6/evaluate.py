import csv
import json
from collections import defaultdict


INPUT_FILE = "experiment6_results.csv"
OUTPUT_FILE = "experiment6_summary.csv"


def safe_average(values):
    """Return average of a list, or 0 if empty."""
    return sum(values) / len(values) if values else 0


def evaluate():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    stats = defaultdict(lambda: {
        "total": 0,
        "category_correct": 0,
        "urgency_correct": 0,
        "sentiment_correct": 0,
        "valid_json": 0,
        "prompt_tokens": [],
        "completion_tokens": [],
        "latency": []
    })

    for row in rows:
        strategy = row["strategy"]
        s = stats[strategy]
        s["total"] += 1

        raw_output = row["raw_output"].strip()

        try:
            prediction = json.loads(raw_output)

            s["valid_json"] += 1

            if prediction.get("category") == row["gold_category"]:
                s["category_correct"] += 1

            if prediction.get("urgency") == row["gold_urgency"]:
                s["urgency_correct"] += 1

            if prediction.get("sentiment") == row["gold_sentiment"]:
                s["sentiment_correct"] += 1

        except (json.JSONDecodeError, TypeError):
            pass

        try:
            s["prompt_tokens"].append(float(row["prompt_tokens"]))
            s["completion_tokens"].append(float(row["completion_tokens"]))
            s["latency"].append(float(row["latency_ms"]))
        except (ValueError, TypeError):
            pass

    summary_rows = []

    print("\n" + "=" * 72)
    print("EXPERIMENT 6 - PROMPTING STRATEGY COMPARISON")
    print("=" * 72)

    for strategy, s in stats.items():
        total = s["total"]

        category_accuracy = s["category_correct"] / total * 100
        urgency_accuracy = s["urgency_correct"] / total * 100
        sentiment_accuracy = s["sentiment_correct"] / total * 100
        json_rate = s["valid_json"] / total * 100

        avg_prompt_tokens = safe_average(s["prompt_tokens"])
        avg_completion_tokens = safe_average(s["completion_tokens"])
        avg_latency = safe_average(s["latency"])

        summary = {
            "strategy": strategy,
            "total_runs": total,
            "category_correct": s["category_correct"],
            "category_accuracy_percent": round(category_accuracy, 2),
            "urgency_correct": s["urgency_correct"],
            "urgency_accuracy_percent": round(urgency_accuracy, 2),
            "sentiment_correct": s["sentiment_correct"],
            "sentiment_accuracy_percent": round(sentiment_accuracy, 2),
            "valid_json": s["valid_json"],
            "valid_json_percent": round(json_rate, 2),
            "avg_prompt_tokens": round(avg_prompt_tokens, 2),
            "avg_completion_tokens": round(avg_completion_tokens, 2),
            "avg_latency_ms": round(avg_latency, 2)
        }

        summary_rows.append(summary)

        print(f"\n{strategy}")
        print("-" * 72)
        print(
            f"Category Accuracy : "
            f"{s['category_correct']}/{total} "
            f"({category_accuracy:.2f}%)"
        )
        print(
            f"Urgency Accuracy  : "
            f"{s['urgency_correct']}/{total} "
            f"({urgency_accuracy:.2f}%)"
        )
        print(
            f"Sentiment Accuracy: "
            f"{s['sentiment_correct']}/{total} "
            f"({sentiment_accuracy:.2f}%)"
        )
        print(
            f"Valid JSON Rate   : "
            f"{s['valid_json']}/{total} "
            f"({json_rate:.2f}%)"
        )
        print(f"Avg Prompt Tokens : {avg_prompt_tokens:.2f}")
        print(f"Avg Completion Tokens: {avg_completion_tokens:.2f}")
        print(f"Avg Latency       : {avg_latency:.2f} ms")

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=summary_rows[0].keys()
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    print("\n" + "=" * 72)
    print(f"Summary saved to: {OUTPUT_FILE}")
    print("=" * 72)


if __name__ == "__main__":
    evaluate()