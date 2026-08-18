[
  {
    "sql": "WITH q1_customers AS (SELECT DISTINCT c.cust_id, c.name FROM customers c JOIN orders o ON c.cust_id = o.cust_id WHERE o.status != 'CANCELLED' AND strftime('%m', o.order_date) BETWEEN '01' AND '03'), q2_customers AS (SELECT DISTINCT c.cust_id FROM customers c JOIN orders o ON c.cust_id = o.cust_id WHERE o.status != 'CANCELLED' AND strftime('%m', o.order_date) BETWEEN '04' AND '06') SELECT q1.cust_id, q1.name FROM q1_customers q1 LEFT JOIN q2_customers q2 ON q1.cust_id = q2.cust_id WHERE q2.cust_id IS NULL"
  }
]