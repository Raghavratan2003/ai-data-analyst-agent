import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.agent import generate_sql, analyze_result
from app.database import run_query
from app.sql_validator import validate_sql
from pandas.api.types import is_numeric_dtype


st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)


st.title("📊 AI Data Analyst")
st.write(
    "Ask questions about the e-commerce database in plain English."
)


question = st.text_input(
    "Ask a data question",
    placeholder="Example: What are the top 5 products by revenue?"
)


if st.button("Analyze"):

    if not question:
        st.warning("Please enter a question.")

    else:

        with st.spinner("Generating SQL..."):

            try:
                sql = generate_sql(question)

            except Exception as e:
                st.error(f"Error generating SQL: {e}")
                st.stop()


        st.subheader("Generated SQL")

        st.code(
            sql,
            language="sql"
        )


        if not validate_sql(sql):

            st.error(
                "The generated SQL was rejected because "
                "only SELECT queries are allowed."
            )

            st.stop()


        with st.spinner("Running query..."):

            try:
                columns, rows = run_query(sql)

            except Exception as e:
                st.error(f"Database error: {e}")
                st.stop()


        st.subheader("Data")

        df = pd.DataFrame(
            rows,
            columns=columns
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        
        
# Visualization
        

        # Visualization
        st.subheader("Visualization")

        if df.empty:
            st.info("No data available to visualize.")

        else:
            # Convert numeric-looking columns, including Decimal values
            for col in df.columns:
                if df[col].dtype == "object":
                    converted = pd.to_numeric(df[col], errors="coerce")

                    if converted.notna().all():
                        df[col] = converted

            numeric_columns = [
                col for col in df.columns
                if is_numeric_dtype(df[col])
                and col.lower() not in ["id", "year"]
                and not col.lower().endswith("_id")
            ]

            category_columns = [
                col for col in df.columns
                if col not in numeric_columns
                and col.lower() != "id"
                and not col.lower().endswith("_id")
            ]

            if numeric_columns and category_columns:
                value_column = numeric_columns[-1]
                category_column = category_columns[0]

                category_name = category_column.lower()

                # Monthly or date-based results
                if any(
                    word in category_name
                    for word in ["month", "date", "time"]
                ):
                    fig = px.line(
                        df,
                        x=category_column,
                        y=value_column,
                        markers=True,
                        title=f"{value_column} over time"
                    )

                # Product, customer, or city rankings
                elif any(
                    word in category_name
                    for word in ["product", "customer", "city"]
                ):
                    fig = px.bar(
                        df,
                        x=value_column,
                        y=category_column,
                        orientation="h",
                        title=f"{value_column} by {category_column}"
                    )

                # Other categorical comparisons
                else:
                    fig = px.bar(
                        df,
                        x=category_column,
                        y=value_column,
                        title=f"{value_column} by {category_column}"
                    )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            elif numeric_columns and len(df) == 1:
                value_column = numeric_columns[0]

                st.metric(
                    label=value_column.replace("_", " ").title(),
                    value=f"{df[value_column].iloc[0]:,.2f}"
                )

            else:
                st.info(
                    "This result does not contain a suitable "
                    "category and numerical measure for a chart."
                )




        with st.spinner("Analyzing results..."):

            try:
                answer = analyze_result(
                    question,
                    columns,
                    rows
                )

            except Exception as e:
                st.error(f"Analysis error: {e}")
                st.stop()


        st.subheader("Analysis")

        st.write(answer)