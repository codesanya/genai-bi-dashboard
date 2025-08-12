"""
Streamlit app: LLM-backed natural language analytics.

Usage:
    1. Set OPENAI_API_KEY in environment (export or .env).
    2. Run create_db.py to create data/sample.db.
    3. Start app: streamlit run app.py
"""
import os
import streamlit as st
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from langchain.chat_models import ChatOpenAI
from langchain.chains import SQLDatabaseChain
from langchain.sql_database import SQLDatabase
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from utils import to_dataframe, choose_chart_and_render

load_dotenv()

DB_PATH = os.path.join("data", "sample.db")

st.set_page_config(page_title="GenAI BI Dashboard", layout="wide")

st.title("GenAI-Powered Business Intelligence Dashboard")
st.markdown("Enterprise-style prototype: ask business questions in plain English and receive visual insights.")

# Ensure DB exists
if not os.path.exists(DB_PATH):
    st.error("Sample database not found. Run `python create_db.py` to generate data/sample.db")
    st.stop()

# Sidebar: model config
st.sidebar.header("Model & Connection")
openai_key = st.sidebar.text_input("OpenAI API Key", type="password")
if not openai_key:
    openai_key = os.environ.get("OPENAI_API_KEY", "")

model_name = st.sidebar.selectbox("LLM Model", ["gpt-4o-mini", "gpt-4o", "gpt-4o-realtime-preview", "gpt-4o-mini-instruct"], index=0)
max_tokens = st.sidebar.slider("Max tokens", 256, 4096, 1024)

if not openai_key:
    st.sidebar.warning("OpenAI API key not set. Set OPENAI_API_KEY in environment or paste here to enable LLM functionality.")

# user query
query = st.text_input("Ask a question about the business data (e.g., 'monthly revenue by region' or 'top 3 products by sales')")
run_query = st.button("Run")

conn = sqlite3.connect(DB_PATH)
engine = create_engine(f"sqlite:///{DB_PATH}")

if run_query and query.strip():
    if not openai_key:
        st.error("LLM unavailable: set OPENAI_API_KEY to enable natural language -> SQL translation.")
    else:
        with st.spinner("Generating SQL and visualizing results..."):
            # instantiate LLM and SQLDatabaseChain
            llm = ChatOpenAI(model=model_name, openai_api_key=openai_key, temperature=0, max_tokens=max_tokens)
            db = SQLDatabase(engine)

            # optional: customize prompt for business context
            prompt = PromptTemplate(
                input_variables=["input"],
                template=(
                    "You are a data analyst assistant. Translate the user's natural language question into a SQL query"
                    " against the sqlite database. Return only the SQL query. Use standard SQL compatible with sqlite. "
                    "If aggregation is required, include GROUP BY. Limit rows to 1000 if no other limit specified. "
                    "Tables: sales(order_id, order_date, customer_id, product, category, quantity, price, region), "
                    "customers(customer_id, name, signup_date, segment, country), "
                    "feedback(feedback_id, customer_id, order_id, rating, comments, created_at)."
                    "\nUser question: {input}"
                )
            )

            chain = SQLDatabaseChain(llm=llm, database=db, verbose=False, prompt=prompt)

            try:
                result = chain.run(query)
                # chain.run returns textual answer by default; try to extract SQL executed
                st.subheader("LLM-generated response")
                st.code(result)

                # Best-effort: run the SQL by asking the LLM for a SQL-only answer is handled via prompt above.
                # For safety, attempt to extract SQL statement from the result text
                sql_text = None
                # naive find: look for 'SELECT' in result
                r = result
                if "select" in r.lower():
                    # extract substring starting at first SELECT
                    idx = r.lower().find("select")
                    sql_text = r[idx:]
                if sql_text:
                    st.subheader("Executing SQL")
                    try:
                        df = pd.read_sql_query(sql_text, conn)
                        if df.empty:
                            st.warning("No data found for the generated query.")
                        else:
                            st.dataframe(df)

                            # Auto chart selection & rendering
                            choose_chart_and_render(df, st)

                    except Exception as exec_err:
                        st.error(f"Error executing SQL: {exec_err}")
                else:
                    st.warning("Could not extract a valid SQL query from LLM output.")

            except Exception as e:
                st.error(f"Error running LLM chain: {e}")
else:
    if run_query and not query.strip():
        st.warning("Please enter a valid question.")

conn.close()
