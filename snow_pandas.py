### function to connect to snowflake for outputting a pandas dataframe
### requires a file in a sibling folder called creds with
### an array of 0)our snowflake account, 1)our warehouse, 2) your username, 3)your password
### function defaults to running sample query listed as sample_query.sql
### this can be changed when used or in test.py (which runs and outputs the df as a sample)
import snowflake.connector
from sqlalchemy import create_engine
from snowflake.connector.pandas_tools import pd_writer
import sys
sys.path.append("..")
from information.creds import setup
import streamlit as st

# Open and read a sample SQL file
f = open('sample_query.sql', 'r')
sql_script = f.read()
f.close()



@st.experimental_memo(ttl=6000)
def snowflake_to_df(sql=sql_script):
	# Connection string
	conn = snowflake.connector.connect(
                user=setup[2],
                password=setup[3],
                account=setup[0],
		warehouse=setup[1]
	)
	cur = conn.cursor()
	cur.execute(sql)
	@st.experimental_memo(ttl=6000)
	try:
		df = cur.fetch_pandas_all()
		cur.close()
		conn.close()
		return df
	except snowflake.connector.errors.NotSupportedError:
		cur.close()
		conn.close()
		return "output not df"
	


def df_to_snowflake(schema,df,table):
	# Connection string
	engine = create_engine(
		'snowflake://{user}:{password}@{account_identifier}/SILAB/{schema_name}?warehouse={warehouse}&role=ACCOUNTADMIN'.format(
		user=setup[2],
		password=setup[3],
		account_identifier=setup[0],
		schema_name = schema,
		warehouse=setup[1],
		)
	)
	conn = engine.connect()
	#cur = conn.cursor()
	#cur.execute("USE DATABASE SILAB")
	#sql1 = "CREATE SCHEMA IF NOT EXISTS " + schema
	#cur.execute(sql1)
	#print("schema created")
	#sql2 = "USE SCHEMA " + schema
	#cur.execute(sql2)
	#sql3 = "CREATE TABLE IF NOT EXISTS " + table 
	#print("table created")
	#cur.execute(sql3)
	df.to_sql(table.lower(), con=conn, if_exists='append', index=False, method = pd_writer)
	#cur.close()
	conn.close()
	return print("Done")

