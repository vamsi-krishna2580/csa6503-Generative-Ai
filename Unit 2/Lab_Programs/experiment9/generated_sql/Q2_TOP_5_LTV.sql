[
  {
    "query": "SELECT c.cust_id, c.name, SUM(oi.qty * p.unit_price * (1.0 - oi.discount_pct / 100.0)) AS lifetime_revenue FROM customers c JOIN orders o ON c.cust_id = o.cust_id JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.prod_id = p.prod_id WHERE o.status != 'CANCELLED' GROUP BY c.cust_id, c.name ORDER BY lifetime_revenue DESC LIMIT 5"
  }
]