import os
import streamlit as st

from dotenv import load_dotenv
from openai import OpenAI

from app.prompts import SQL_SYSTEM_PROMPT, ANALYSIS_SYSTEM_PROMPT

load_dotenv()

api_key = (
    os.getenv("OPENAI_API_KEY")
    or st.secrets.get("OPENAI_API_KEY")
)

client = OpenAI(api_key=api_key)


def generate_sql(question):

    response = client.responses.create(
        model="gpt-5-nano",
        instructions=SQL_SYSTEM_PROMPT,
        input=question
    )

    sql = response.output_text.strip()

    return sql


def analyze_result(question, columns, rows):

    result_text = str(rows)

    response = client.responses.create(
        model="gpt-5-nano",
        instructions=ANALYSIS_SYSTEM_PROMPT,
        input=f"""
User question:

{question}

Query result columns:

{columns}

Query result:

{result_text}
"""
    )

    return response.output_text.strip()