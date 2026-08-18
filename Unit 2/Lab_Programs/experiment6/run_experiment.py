import csv
import time
import pandas as pd

from prompts import (
    zero_shot_prompt,
    one_shot_prompt,
    few_shot_prompt
)
from llm_client import call_llm


OUTPUT_FILE = "experiment6_results.csv"

STRATEGIES = {
    "ZERO_SHOT": zero_shot_prompt,
    "ONE_SHOT": one_shot_prompt,
    "FEW_SHOT": few_shot_prompt
}


def is_failed(value):
    """Check whether a previous request failed."""
    if pd.isna(value):
        return True

    value = str(value).strip()

    return (
        value == ""
        or value.lower() == "nan"
        or value.startswith("ERROR")
    )


def main():
    df = pd.read_csv(OUTPUT_FILE)

    failed_indices = df[
        df["raw_output"].apply(is_failed)
    ].index.tolist()

    print(f"Total rows in CSV: {len(df)}")
    print(f"Failed rows found: {len(failed_indices)}")

    if not failed_indices:
        print("No failed rows. Nothing to retry.")
        return

    for index in failed_indices:
        row = df.loc[index]

        strategy = row["strategy"]
        message_id = row["id"]
        message = row["message"]

        print(
            f"\nRetrying row {index}: "
            f"{strategy} - {message_id}"
        )

        prompt_function = STRATEGIES[strategy]
        prompt = prompt_function(message)

        while True:
            try:
                response = call_llm(
                    prompt=prompt,
                    temperature=0.2,
                    top_p=1.0,
                    max_tokens=150
                )

                df.loc[index, "raw_output"] = response["text"]
                df.loc[index, "prompt_tokens"] = response["prompt_tokens"]
                df.loc[index, "completion_tokens"] = response["completion_tokens"]
                df.loc[index, "latency_ms"] = response["latency_ms"]

                # Save immediately after every successful retry
                df.to_csv(
                    OUTPUT_FILE,
                    index=False,
                    encoding="utf-8"
                )

                print("SUCCESS")
                print(response["text"])

                time.sleep(2)
                break

            except Exception as error:
                error_text = str(error)

                print("ERROR:", error_text)

                if (
                    "429" in error_text
                    or "RESOURCE_EXHAUSTED" in error_text
                ):
                    print("Rate limit reached. Waiting 60 seconds...")
                    time.sleep(60)
                else:
                    print("Skipping this row for now.")
                    break

    print("\nFinished retrying failed rows.")

    # Final check
    df = pd.read_csv(OUTPUT_FILE)

    remaining = df[
        df["raw_output"].apply(is_failed)
    ]

    print(f"Remaining failed rows: {len(remaining)}")

    if len(remaining) == 0:
        print("SUCCESS: All rows are now completed!")
    else:
        print("Some rows still need retrying:")
        print(remaining[["strategy", "id", "raw_output"]])


if __name__ == "__main__":
    main()