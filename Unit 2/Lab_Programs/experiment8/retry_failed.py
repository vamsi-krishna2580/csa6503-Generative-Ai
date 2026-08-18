import csv
import json
import pandas as pd

from data import FARMER_PROFILES
from advisory import generate_advisory


INPUT_FILE = "experiment8_results.csv"


def get_sms(text):
    text = str(text).strip()

    try:
        data = json.loads(text)
        if isinstance(data, dict) and "sms" in data:
            return str(data["sms"]).strip()
    except Exception:
        pass

    return text.strip().strip('"')


def main():

    df = pd.read_csv(INPUT_FILE)

    failed_ids = []

    for index, row in df.iterrows():
        if row["experiment_type"] == "BATCH":
            sms = get_sms(row["advisory"])

            # Update old JSON outputs
            df.at[index, "advisory"] = sms
            df.at[index, "characters"] = len(sms)

            if len(sms) > 160:
                failed_ids.append(row["profile_id"])

    print("Failed profiles:", failed_ids)

    profile_map = {
        profile["id"]: profile
        for profile in FARMER_PROFILES
    }

    for index, row in df.iterrows():

        if (
            row["experiment_type"] == "BATCH"
            and row["profile_id"] in failed_ids
        ):

            profile = profile_map[row["profile_id"]]

            print(
                f"\nRetrying {profile['id']} - "
                f"{profile['crop']}"
            )

            result = generate_advisory(
                profile,
                temperature=0.2,
                top_p=0.5
            )

            df.at[index, "advisory"] = result["text"]
            df.at[index, "characters"] = len(result["text"])
            df.at[index, "latency_ms"] = result["latency_ms"]
            df.at[index, "prompt_tokens"] = result["prompt_tokens"]
            df.at[index, "completion_tokens"] = result["completion_tokens"]
            df.at[index, "attempts"] = result["attempts"]
            df.at[index, "fallback_used"] = result["fallback_used"]

            print("Characters:", len(result["text"]))
            print("SMS:", result["text"])

    # Also clean parameter sweep rows
    for index, row in df.iterrows():
        if row["experiment_type"] == "PARAMETER_SWEEP":
            sms = get_sms(row["advisory"])
            df.at[index, "advisory"] = sms
            df.at[index, "characters"] = len(sms)

    df.to_csv(INPUT_FILE, index=False)

    print("\nUpdated experiment8_results.csv")

    remaining = df[
        (df["experiment_type"] == "BATCH")
        & (df["characters"] > 160)
    ]

    print("Remaining over 160 characters:", len(remaining))

    if len(remaining) == 0:
        print("SUCCESS: All batch advisories satisfy the SMS limit.")


if __name__ == "__main__":
    main()