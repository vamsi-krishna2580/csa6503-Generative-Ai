import csv
import re


INPUT_FILE = "experiment7_results.csv"


def load_source():
    with open("source_text.txt", "r", encoding="utf-8") as f:
        return f.read()


def get_words(text):
    return re.findall(r"\b[\w-]+\b", str(text))


def word_count(text):
    return len(get_words(text))


def extract_numbers(text):
    return set(re.findall(r"\b\d+(?:\.\d+)?%?\b", text))


def extract_dates(text):
    months = (
        r"January|February|March|April|May|June|"
        r"July|August|September|October|November|December"
    )

    pattern = rf"\b\d{{1,2}}\s+(?:{months})(?:\s+\d{{4}})?\b"

    return set(re.findall(pattern, text))


def hallucination_check(source, output):
    """
    Basic automatic candidate check.
    Final hallucination count must be manually verified.
    """

    source_numbers = extract_numbers(source)
    output_numbers = extract_numbers(output)

    source_dates = extract_dates(source)
    output_dates = extract_dates(output)

    suspicious_numbers = output_numbers - source_numbers
    suspicious_dates = output_dates - source_dates

    return (
        len(suspicious_numbers) + len(suspicious_dates),
        suspicious_numbers,
        suspicious_dates
    )


def print_section(title):
    print("\n" + "=" * 75)
    print(title)
    print("=" * 75)


def main():
    source = load_source()
    source_tokens = word_count(source)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print_section("EXPERIMENT 7 EVALUATION")
    print(f"Source word count: {source_tokens}")

    evaluation_rows = []

    summary_tasks = {
        "Executive Abstract",
        "Action-Item List",
        "Technical Summary"
    }

    for row in rows:
        task = row["task"]
        output = row["output"]

        output_tokens = word_count(output)

        if task in summary_tasks:
            compression = output_tokens / source_tokens
            hall_count, numbers, dates = hallucination_check(
                source,
                output
            )
        else:
            compression = ""
            hall_count = ""
            numbers = set()
            dates = set()

        evaluation_rows.append({
            "task": task,
            "output_length_words": output_tokens,
            "compression_ratio": (
                round(compression, 4)
                if compression != ""
                else ""
            ),
            "auto_hallucination_candidates": hall_count,
            "suspicious_numbers": ", ".join(sorted(numbers)),
            "suspicious_dates": ", ".join(sorted(dates))
        })

        print(f"\nTASK: {task}")
        print(f"Output length: {output_tokens} words")

        if compression != "":
            print(f"Compression ratio: {compression:.4f}")
            print(
                "Possible hallucination candidates: "
                f"{hall_count}"
            )

            if numbers:
                print(
                    "Numbers requiring manual verification:",
                    numbers
                )

            if dates:
                print(
                    "Dates requiring manual verification:",
                    dates
                )

    with open(
        "experiment7_evaluation.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=evaluation_rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(evaluation_rows)

    print_section("SAVED")
    print("experiment7_evaluation.csv")
    print("\nIMPORTANT:")
    print(
        "Hallucination candidates are only an automatic check."
    )
    print(
        "Manually verify names, numbers and dates against source_text.txt."
    )


if __name__ == "__main__":
    main()