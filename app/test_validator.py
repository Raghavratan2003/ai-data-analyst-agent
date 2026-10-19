
from sql_validator import validate_sql, prepare_sql


def test_valid_select():
    query = "SELECT product_name FROM products"
    assert validate_sql(query) is True


def test_reject_delete():
    query = "DELETE FROM products"
    assert validate_sql(query) is False


def test_reject_multiple_statements():
    query = "SELECT * FROM products; DROP TABLE products"
    assert validate_sql(query) is False


def test_adds_limit():
    query = prepare_sql("SELECT * FROM products")
    assert "LIMIT 1000" in query.upper()


def test_preserves_existing_limit():
    query = prepare_sql("SELECT * FROM products LIMIT 10")
    assert "LIMIT 10" in query.upper()


if __name__ == "__main__":
    test_valid_select()
    test_reject_delete()
    test_reject_multiple_statements()
    test_adds_limit()
    test_preserves_existing_limit()

    print("All SQL validator tests passed.")
