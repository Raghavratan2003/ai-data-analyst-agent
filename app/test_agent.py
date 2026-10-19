from agent import generate_sql


question = "What are the top 5 products by revenue?"

sql = generate_sql(question)

print("Generated SQL:")
print(sql)