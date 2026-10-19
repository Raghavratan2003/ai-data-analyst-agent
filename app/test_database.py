from database import run_query


query = """
SELECT
    p.category,
    SUM(oi.revenue) AS total_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
"""


columns, rows = run_query(query)

print(columns)

for row in rows:
    print(row)