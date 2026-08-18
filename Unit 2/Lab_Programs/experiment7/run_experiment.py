import csv
import time

from llm_client import call_llm
from prompts import (
    executive_prompt,
    action_prompt,
    technical_prompt,
    email_prompt,
    content_prompt,
    ablation_prompt
)


def load_source():
    with open("source_text.txt", "r", encoding="utf-8") as f:
        return f.read()


def run_task(name, prompt, results):
    print(f"Running: {name}")

    response = call_llm(
        prompt=prompt,
        temperature=0.2,
        top_p=1.0,
        max_tokens=1000
    )

    results.append({
        "task": name,
        "output": response["text"],
        "prompt_tokens": response["prompt_tokens"],
        "completion_tokens": response["completion_tokens"],
        "latency_ms": response["latency_ms"]
    })

    print("DONE")
    time.sleep(2)


def main():
    source = load_source()
    results = []

    # PART 7A
    run_task(
        "Executive Abstract",
        executive_prompt(source),
        results
    )

    run_task(
        "Action-Item List",
        action_prompt(source),
        results
    )

    run_task(
        "Technical Summary",
        technical_prompt(source),
        results
    )

    # PART 7B
    run_task(
        "Email - Formal",
        email_prompt("Formal, professional and accountable."),
        results
    )

    run_task(
        "Email - Empathetic",
        email_prompt(
            "Empathetic and understanding, while remaining professional and accountable."
        ),
        results
    )

    run_task(
        "Email - Assertive",
        email_prompt(
            "Assertive, confident, professional and solution-focused."
        ),
        results
    )

    # PART 7C
    run_task(
        "Product Launch Campaign",
        content_prompt(),
        results
    )

    # ABLATION STUDY
    for component in [
        "ROLE",
        "CONTEXT",
        "TONE",
        "WORD_COUNT",
        "OUTPUT_FORMAT"
    ]:
        run_task(
            f"Ablation - Remove {component}",
            ablation_prompt(component),
            results
        )

    with open(
        "experiment7_results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=results[0].keys()
        )

        writer.writeheader()
        writer.writerows(results)

    print("\n=================================")
    print("EXPERIMENT 7 COMPLETED")
    print(f"Total tasks: {len(results)}")
    print("Saved: experiment7_results.csv")
    print("=================================")


if __name__ == "__main__":
    main()