import csv
import pandas as pd


INPUT_FILE = "experiment8_results.csv"


def factual_safety(row):

    advisory = str(row["advisory"]).lower()
    crop = str(row["crop"]).lower()

    # Basic automatic checks
    if len(advisory) > 160:
        return "NO - exceeds 160 characters"

    if crop not in advisory:
        return "CHECK MANUALLY"

    return "CHECK MANUALLY"


def main():

    df = pd.read_csv(INPUT_FILE)

    sweep = df[
        df["experiment_type"] == "PARAMETER_SWEEP"
    ].copy()

    batch = df[
        df["experiment_type"] == "BATCH"
    ].copy()

    sweep["factually_safe"] = sweep.apply(
        factual_safety,
        axis=1
    )

    print("\n========================================")
    print("EXPERIMENT 8 - PARAMETER SWEEP")
    print("========================================\n")

    print(
        sweep[
            [
                "temperature",
                "top_p",
                "advisory",
                "characters",
                "latency_ms",
                "factually_safe"
            ]
        ].to_string(index=False)
    )

    print("\n========================================")
    print("BATCH GENERATION SUMMARY")
    print("========================================")

    print(f"Total profiles: {len(batch)}")
    print(
        f"Average characters: "
        f"{batch['characters'].mean():.2f}"
    )
    print(
        f"Average latency: "
        f"{batch['latency_ms'].mean():.2f} ms"
    )
    print(
        f"Average prompt tokens: "
        f"{batch['prompt_tokens'].mean():.2f}"
    )
    print(
        f"Average completion tokens: "
        f"{batch['completion_tokens'].mean():.2f}"
    )
    print(
        f"Fallbacks used: "
        f"{batch['fallback_used'].sum()}"
    )

    sweep.to_csv(
        "experiment8_parameter_sweep.csv",
        index=False
    )

    print("\nSaved: experiment8_parameter_sweep.csv")


if __name__ == "__main__":
    main()