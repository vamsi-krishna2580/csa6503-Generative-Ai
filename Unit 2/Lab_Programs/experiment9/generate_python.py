from llm_client import call_llm


PYTHON_PROMPT_V1 = """
You are an expert Python data engineer.

Generate one complete executable Python module named sales_report.py.

DATABASE:
SQLite file: retail.db

DATABASE SCHEMA:

customers(cust_id, name, city, join_date, segment)
products(prod_id, name, category, unit_price)
orders(order_id, cust_id, order_date, status)
order_items(order_id, prod_id, qty, discount_pct)

BUSINESS RULES:
- Revenue = qty * unit_price * (1 - discount_pct / 100.0)
- Exclude orders where status = 'CANCELLED'

TASK:
1. Connect to retail.db using sqlite3.
2. Compute category-wise revenue summary.
3. Include category and total revenue.
4. Export the summary to sales_report.xlsx.
5. Create a bar chart from the summary.
6. The Excel file must contain the revenue data and chart.

CONSTRAINTS:
- Type hints on ALL functions.
- Docstrings on ALL functions.
- PEP-8 compliant.
- Use only sqlite3 and pandas for database/data processing.
- Use parameterised SQL queries only.
- Do not concatenate user input into SQL.
- Do not use external database libraries.
- Include:
  if __name__ == "__main__":
- The program must run from the same folder as retail.db.
- Return ONLY Python code.
- No Markdown fences.
- No explanation.
"""


def clean_code(text: str) -> str:
    """Remove accidental Markdown fences."""

    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        lines = lines[1:]

        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]

        text = "\n".join(lines)

    return text.strip()


def main() -> None:
    """Generate sales_report.py version 1."""

    response = call_llm(
        prompt=PYTHON_PROMPT_V1,
        temperature=0.0,
        top_p=1.0,
        max_tokens=2000
    )

    code = clean_code(response["text"])

    with open(
        "sales_report.py",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(code)

    with open(
        "prompt_v1.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(PYTHON_PROMPT_V1)

    print("Generated sales_report.py")
    print("Saved prompt_v1.txt")


if __name__ == "__main__":
    main()