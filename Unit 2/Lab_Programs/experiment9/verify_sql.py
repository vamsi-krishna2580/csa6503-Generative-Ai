import csv
import sqlite3
from pathlib import Path


DB_NAME = "retail.db"
SQL_DIR = Path("generated_sql")


def main() -> None:
    """Execute every generated SQL query and log results."""

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    results = []

    for sql_file in sorted(SQL_DIR.glob("*.sql")):

        artefact = sql_file.stem
        sql = sql_file.read_text(encoding="utf-8")

        print("\n" + "=" * 70)
        print("VERIFYING:", artefact)
        print("=" * 70)

        try:
            cursor.execute(sql)
            rows = cursor.fetchall()

            print("SUCCESS")
            print("Rows returned:", len(rows))

            results.append({
                "artefact": artefact,
                "runs_first_try": "YES",
                "attempts_to_fix": 0,
                "error_class": "",
                "root_cause": "",
                "verification": "EXECUTED_SUCCESSFULLY",
                "rows_returned": len(rows)
            })

        except Exception as error:

            print("FAILED:", type(error).__name__)
            print("CAUSE:", str(error))

            results.append({
                "artefact": artefact,
                "runs_first_try": "NO",
                "attempts_to_fix": 1,
                "error_class": type(error).__name__,
                "root_cause": str(error),
                "verification": "FAILED_EXECUTION",
                "rows_returned": 0
            })

    conn.close()

    with open(
        "sql_verification_log.csv",
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

    print("\nSaved: sql_verification_log.csv")


if __name__ == "__main__":
    main()