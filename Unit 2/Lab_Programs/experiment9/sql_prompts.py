SCHEMA = """
DATABASE SCHEMA:

customers(
    cust_id,
    name,
    city,
    join_date,
    segment
)

products(
    prod_id,
    name,
    category,
    unit_price
)

orders(
    order_id,
    cust_id,
    order_date,
    status
)

order_items(
    order_id,
    prod_id,
    qty,
    discount_pct
)
"""


RULES = """
BUSINESS RULES:
- SQL dialect: SQLite.
- Revenue = qty * unit_price * (1 - discount_pct / 100.0).
- Valid orders exclude status = 'CANCELLED'.
- Never invent columns.
- Use only tables and columns listed in the schema.
- Do not use SELECT *.
- Use CTEs where intermediate calculations are needed.
- Alias every aggregate expression.
- Return only executable SQL.
- No markdown.
- No explanation.
"""


QUESTIONS = {
    "Q1_MOM_GROWTH": """
Generate SQLite SQL for:

Month-over-month revenue growth per product category
for the last twelve months.

Return category, month, monthly revenue, previous month revenue,
and percentage growth.

Handle the first month, where no previous month exists,
without division by zero.
""",

    "Q2_TOP_5_LTV": """
Generate SQLite SQL for:

Top five customers by lifetime value.

Exclude CANCELLED orders.

Return customer ID, customer name and lifetime revenue,
ordered from highest to lowest revenue.
""",

    "Q3_QOQ_DROP": """
Generate SQLite SQL for:

Products whose sales revenue dropped by more than 30 percent
quarter-over-quarter.

Compare each product's current quarter revenue with its
immediately previous quarter revenue.

Return product ID, product name, current quarter,
current revenue, previous quarter revenue and percentage drop.
""",

    "Q4_CHURN": """
Generate SQLite SQL for:

Customers who purchased in Q1 but did not purchase in Q2.

Treat purchases as valid orders only.
Use the same calendar year for Q1 and Q2.

Return customer ID and customer name.
"""
}


def build_prompt(question: str) -> str:
    """Build a schema-grounded SQL generation prompt."""

    return f"""
You are an expert SQL developer.

{SCHEMA}

{RULES}

TASK:
{question}
"""