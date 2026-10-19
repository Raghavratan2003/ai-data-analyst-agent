
import os

import psycopg2
from dotenv import load_dotenv

from app.sql_validator import prepare_sql


load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "ai_analyst"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}


def get_connection():
    if not DB_CONFIG["password"]:
        raise ValueError("DB_PASSWORD is missing from .env")

    return psycopg2.connect(**DB_CONFIG)



def run_query(query):
    safe_query = prepare_sql(query)

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("SET statement_timeout = '10s'")
            cursor.execute("SET TRANSACTION READ ONLY")

            cursor.execute(safe_query)

            if cursor.description is None:
                raise ValueError("Query returned no result set.")

            columns = [
                column[0] for column in cursor.description
            ]

            rows = cursor.fetchmany(1000)

        return columns, rows

    finally:
        conn.rollback()
        conn.close()
