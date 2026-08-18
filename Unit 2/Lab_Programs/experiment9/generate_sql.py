import csv
import os

from llm_client import call_llm
from sql_prompts import QUESTIONS, build_prompt


def clean_sql(text: str) -> str:
    """Remove accidental Markdown SQL fences."""

    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        if lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]

        text = "\n".join(lines)

    return text.strip()


def main() -> None:
    """Generate four SQL queries and save them."""

    os.makedirs("generated_sql", exist_ok=True)

    rows = []

    for name, question in QUESTIONS.items():

        print(f"\nGenerating {name}...")

        response = call_llm(
            prompt=build_prompt(question),
            temperature=0.0,
            top_p=1.0,
            max_tokens=1200
        )

        sql = clean_sql(response["text"])

        file_name = f"generated_sql/{name}.sql"

        with open(file_name, "w", encoding="utf-8") as file:
            file.write(sql)

        rows.append({
            "artefact": name,
            "attempt": 1,
            "sql_file": file_name,
            "prompt_tokens": response["prompt_tokens"],
            "completion_tokens": response["completion_tokens"],
            "latency_ms": response["latency_ms"]
        })

        print("Saved:", file_name)

    with open(
        "sql_generation_log.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)

    print("\nAll SQL queries generated.")


if __name__ == "__main__":
    main()