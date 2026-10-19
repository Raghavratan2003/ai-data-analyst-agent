from agent import generate_sql, analyze_result
from database import run_query
from sql_validator import validate_sql


question = input("Ask a data question: ")

print("\nGenerating SQL...")

sql = generate_sql(question)

print("\nGenerated SQL:")
print(sql)


if not validate_sql(sql):
    print("\nInvalid SQL. Only SELECT queries are allowed.")
    exit()


print("\nExecuting query...")

columns, rows = run_query(sql)

print("\nRaw result:")
print(columns)

for row in rows:
    print(row)


print("\nAnalyzing result...")

answer = analyze_result(
    question,
    columns,
    rows
)

print("\nAnswer:")
print(answer)