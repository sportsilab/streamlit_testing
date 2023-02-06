import streamlit as st
import snowflake.connector
from snowflake.connector.pandas_tools import pd_writer
import sys
sys.path.append("..")
from information.creds import setup


# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(
        user=setup[2],
        password=setup[3],
        account=setup[0],
	warehouse=setup[1], 
	client_session_keep_alive=True
    )

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after an hour.
@st.experimental_memo(ttl=3600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetch_pandas_all()
