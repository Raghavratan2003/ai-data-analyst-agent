# AI Data Analyst Agent

An AI-powered data analytics application that converts natural-language questions into SQL queries, executes them against a PostgreSQL database, and presents the results through interactive visualizations and AI-generated explanations.

## Overview

Business users often need SQL knowledge to retrieve insights from relational databases. This project simplifies that process by allowing users to ask analytical questions in plain English.

**Example question:**

> What are the top 10 products by revenue?

The application generates SQL, validates the query, retrieves the data, and presents the results in a table, chart, and natural-language explanation.

## Features

- **Natural Language to SQL:** Generate PostgreSQL queries from user questions using an OpenAI model.
- **SQL Validation:** Parse and validate generated SQL before execution.
- **Database Integration:** Query a PostgreSQL e-commerce database.
- **Data Analysis:** Generate concise explanations from query results.
- **Interactive Visualizations:** Display charts using Plotly.
- **Streamlit Interface:** Interact with the system through a simple web application.
- **Database Safeguards:** Use a read-only database account, query timeouts, and result limits.
- **Automated Tests:** Test core SQL validation behavior.

## Architecture

```text
User Question
     |
     v
Streamlit Interface
     |
     v
LLM - SQL Generation
     |
     v
SQL Validation
     |
     v
PostgreSQL Database
     |
     v
Pandas DataFrame
     |
     +------------------+
     |                  |
     v                  v
Plotly Visualization  LLM Analysis
     |                  |
     +---------+--------+
               |
               v
       Results and Insights
```

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| User interface | Streamlit |
| API integration | OpenAI API |
| Database | PostgreSQL |
| Data processing | Pandas |
| Visualization | Plotly |
| SQL parsing | SQLGlot |
| Database connectivity | Psycopg2 |

## Database Schema

The project uses an e-commerce database with four related tables:

- `customers`: Customer information and location.
- `products`: Product names, categories, and prices.
- `orders`: Order dates, customers, and order totals.
- `order_items`: Products purchased, quantities, and item revenue.

These relationships support analytical queries involving joins, aggregations, date filtering, and rankings.

## Example Questions

- What are the top 10 products by revenue?
- Which product category generated the most revenue?
- Show monthly revenue for 2025.
- Which city has the highest number of customers?
- Compare revenue between 2024 and 2025.
- What is the total revenue by product category?

## Project Structure

```text
ai-data-analyst-agent/
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── database.py
│   ├── prompts.py
│   ├── sql_validator.py
│   └── test_validator.py
├── data/
│   └── generate_data.py
├── frontend/
│   └── dashboard.py
├── sql/
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

The exact files may vary slightly depending on your local setup.


## Application Preview

![AI Data Analyst dashboard](screenshots/dashboard1.png)
![SQL query results](screenshots/dashboard2.png)
![Data](screenshots/dashboard3.png)
![Data visualization](screenshots/dashboard4.png)
![Analysis output](screenshots/dashboard5.png)

## Local Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ai-data-analyst-agent
```

### 2. Install dependencies

Install [uv](https://docs.astral.sh/uv/) if necessary, then run:

```bash
uv sync
```

If your project dependencies have not yet been recorded in `pyproject.toml`, add the packages used by the application before running `uv sync`.

### 3. Configure environment variables

Create a `.env` file in the project root:

```dotenv
OPENAI_API_KEY=your_openai_api_key
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ai_analyst
DB_USER=ai_analyst_reader
DB_PASSWORD=your_database_password
```

Never commit real API keys or passwords.

### 4. Set up PostgreSQL

Install and start PostgreSQL. Create the `ai_analyst` database and the four tables described above.

Create a dedicated database account with read-only access to the required tables.

### 5. Generate sample data

Configure the database connection in your data-generation script and run:

```bash
uv run python data/generate_data.py
```

Run this only when the database tables are empty or when you have intentionally prepared them for a fresh data load.

### 6. Launch the application

From the project root:

```bash
uv run python -m streamlit run frontend/dashboard.py
```

Open the local URL displayed in the terminal.

### 7. Run tests

```bash
uv run python app/test_validator.py
```

## Security Considerations

- API keys and database credentials are stored in environment variables.
- SQL queries are parsed and restricted before execution.
- The application uses a read-only database account.
- Query execution has a timeout and a result-row limit.
- SQL validation alone is not a complete security boundary. Further restrictions are needed before exposing the application to untrusted users or sensitive databases.

## Limitations

- Generated SQL can be syntactically valid but analytically incorrect.
- Chart selection uses heuristics and may not always choose the best visualization.
- The sample dataset is synthetic and does not represent real business performance.
- Model usage requires an accessible OpenAI API account and may incur API charges.
- The application is a portfolio prototype, not a production-grade enterprise analytics platform.

## Future Improvements

- Improve SQL generation using representative question-query examples.
- Add automated tests for generated SQL and analytical correctness.
- Improve chart selection based on data types and query intent.
- Add query history and CSV export.
- Deploy the application with secure secrets management.

## Author

**Raghav Ratan Yadav**

Integrated M.Sc. Mathematics | Data Analytics | Python | SQL | PostgreSQL | Generative AI
