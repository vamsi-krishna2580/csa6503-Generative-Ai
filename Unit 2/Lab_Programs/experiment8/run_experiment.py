import csv
import time

from data import FARMER_PROFILES
from advisory import generate_advisory


SWEEP_SETTINGS = [
    {"temperature": 0.0, "top_p": 1.0},
    {"temperature": 0.4, "top_p": 1.0},
    {"temperature": 0.9, "top_p": 1.0},
    {"temperature": 0.4, "top_p": 0.5},
    {"temperature": 0.9, "top_p": 0.5}
]


def main():

    results = []

    # Same advisory for parameter sweep
    test_profile = FARMER_PROFILES[0]

    print("\n====================================")
    print("PARAMETER SWEEP")
    print("====================================")

    for setting in SWEEP_SETTINGS:

        temperature = setting["temperature"]
        top_p = setting["top_p"]

        print(
            f"\nTemperature={temperature}, Top_P={top_p}"
        )

        result = generate_advisory(
            test_profile,
            temperature=temperature,
            top_p=top_p
        )

        results.append({
            "experiment_type": "PARAMETER_SWEEP",
            "profile_id": test_profile["id"],
            "crop": test_profile["crop"],
            "district": test_profile["district"],
            "weather": test_profile["weather"],
            "temperature": temperature,
            "top_p": top_p,
            "advisory": result["text"],
            "characters": len(result["text"]),
            "latency_ms": result["latency_ms"],
            "prompt_tokens": result["prompt_tokens"],
            "completion_tokens": result["completion_tokens"],
            "attempts": result["attempts"],
            "fallback_used": result["fallback_used"]
        })

        print("Output:", result["text"])
        print("Characters:", len(result["text"]))

        time.sleep(2)

    # Batch generation
    print("\n====================================")
    print("BATCH GENERATION - 10 FARMERS")
    print("====================================")

    for profile in FARMER_PROFILES:

        print(
            f"Generating {profile['id']} - {profile['crop']}..."
        )

        result = generate_advisory(
            profile,
            temperature=0.4,
            top_p=1.0
        )

        results.append({
            "experiment_type": "BATCH",
            "profile_id": profile["id"],
            "crop": profile["crop"],
            "district": profile["district"],
            "weather": profile["weather"],
            "temperature": 0.4,
            "top_p": 1.0,
            "advisory": result["text"],
            "characters": len(result["text"]),
            "latency_ms": result["latency_ms"],
            "prompt_tokens": result["prompt_tokens"],
            "completion_tokens": result["completion_tokens"],
            "attempts": result["attempts"],
            "fallback_used": result["fallback_used"]
        })

        print(
            f"{profile['id']} DONE: "
            f"{len(result['text'])} characters"
        )

        time.sleep(2)

    with open(
        "experiment8_results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )

        writer.writeheader()
        writer.writerows(results)

    print("\n====================================")
    print("EXPERIMENT 8 COMPLETED")
    print(f"Total generations: {len(results)}")
    print("Parameter sweep: 5")
    print("Batch generation: 10")
    print("Saved: experiment8_results.csv")
    print("====================================")


if __name__ == "__main__":
    main()