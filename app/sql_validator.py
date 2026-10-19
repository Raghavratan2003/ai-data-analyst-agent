
import sqlglot
from sqlglot import exp


MAX_ROWS = 1000


def validate_sql(query):
    try:
        statements = sqlglot.parse(query, read="postgres")

        # Require exactly one valid statement.
        if len(statements) != 1 or statements[0] is None:
            return False

        statement = statements[0]

        # Accept SELECT-style queries, including UNION.
        if not isinstance(statement, exp.Query):
            return False

        # Reject SELECT INTO and row-locking queries.
        if statement.find(exp.Into):
            return False

        if statement.find(exp.Lock):
            return False

        return True

    except Exception:
        return False


def prepare_sql(query):
    """Validate SQL and enforce a maximum output row count."""
    if not validate_sql(query):
        raise ValueError("Invalid or unsafe SQL query.")

    statement = sqlglot.parse_one(query, read="postgres")

    # Add a SQL-level limit if one is not already present.
    if statement.args.get("limit") is None:
        statement = statement.limit(MAX_ROWS, copy=False)

    return statement.sql(dialect="postgres")
