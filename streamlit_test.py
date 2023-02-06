import streamlit as st
import pandas as pd
import snow_pandas_streamlit
from babel.numbers import format_currency


#initiate the connection
conn = snow_pandas_streamlit.init_connection()


f = open('dc_team_grouping_query.sql', 'r')
sql_script = f.read()
f.close()

# run the query for the teams
df = snow_pandas_streamlit.run_query(sql_script)

# run the query for the general pop
df_main = snow_pandas_streamlit.run_query("SELECT CATEGORY, SUBCATEGORY, FAN_COUNT, MEDIAN_SPEND_PER_FAN FROM SILAB.FAN_JOURNEY.F_SUMMARY_CATEGORY")

df_short = df[['FAN_GROUPING', 'CATEGORY', 'SUBCATEGORY', 'FAN_COUNT', 'MEDIAN_SPEND_PER_FAN']]

option = st.selectbox(
    'Which DC team would you like to compare to the general population?',
    ('dc_united', 'washington_capitals', 'washington_commanders', 'washington_mystics', 'washington_nationals', 'washington_spirit', 'washington_wizards'))


df_total = pd.merge(df_main, df_short[df_short.FAN_GROUPING == option], on = "SUBCATEGORY")


df_total["COLUMN_DIFF"] = df_total["MEDIAN_SPEND_PER_FAN_y"].astype('float') - df_total["MEDIAN_SPEND_PER_FAN_x"].astype('float')

df_total = df_total.sort_values(by='COLUMN_DIFF', ascending=False)

df_total = df_total[['SUBCATEGORY', 'FAN_COUNT_x', 'MEDIAN_SPEND_PER_FAN_x', 'FAN_COUNT_y', 'MEDIAN_SPEND_PER_FAN_y', 'COLUMN_DIFF']]

df_total = df_total.rename(columns={"FAN_COUNT_x":"GEN_POP_FAN_COUNT", "MEDIAN_SPEND_PER_FAN_x": "GEN_POP_MEDIAN_SPEND_PER_FAN", "FAN_COUNT_y":"TEAM_FAN_COUNT", "MEDIAN_SPEND_PER_FAN_y": "TEAM_MEDIAN_SPEND_PER_FAN"})

df_total["GEN_POP_MEDIAN_SPEND_PER_FAN"] = df_total["GEN_POP_MEDIAN_SPEND_PER_FAN"].apply(lambda x: format_currency(x, currency="USD", locale="en_US"))
df_total["TEAM_MEDIAN_SPEND_PER_FAN"] = df_total["TEAM_MEDIAN_SPEND_PER_FAN"].apply(lambda x: format_currency(x, currency="USD", locale="en_US"))
df_total["COLUMN_DIFF"] = df_total["COLUMN_DIFF"].apply(lambda x: format_currency(x, currency="USD", locale="en_US"))

st.dataframe(df_total)
