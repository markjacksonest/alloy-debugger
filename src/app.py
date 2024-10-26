from datetime import datetime
from typing import List

import streamlit as st
import pandas as pd
# import polars as pl

from src.sql_queries import create_seed_id_query_from_pricing_service_log_table, PricingServiceLogTable
from src.utils.snowflake_db import SnowflakeDb

snowflake_db = SnowflakeDb()
conn = snowflake_db.get_snowflake_connector_with_token()
@st.cache_data
def query_seed_ids(
    seed_ids: List[str],
    table_name: PricingServiceLogTable = None,
    date: datetime.date = None
) -> pd.DataFrame:
    query = create_seed_id_query_from_pricing_service_log_table(seed_ids, table_name=table_name, date=date)
    return pd.read_sql(query, conn)
    # return pl.read_database(query, conn)

st.write("Here's our first attempt at using data to create a table:")
table = st.selectbox('Environment', options=PricingServiceLogTable, format_func=lambda x: x.name)
date = st.date_input('start date', format='YYYY-MM-DD')
seed_ids_input = st.text_input('Comma delimited list of seed ids')

if st.button("Run it again"):
    print('looking for')
    print('seed_ids', seed_ids_input)
    print('table', table)
    print('date', date, type(date))
    seed_ids = list(map(lambda x: x.strip(), seed_ids_input.split(',')))
    df = query_seed_ids(seed_ids, table_name=table, date=date)
    df['has_output'] = ~df.OUTPUT_OBJ.isna()
    seed_ids_runs_df = df[['ID', 'SEED_ID', 'has_output', 'CREATION_TS']]
    seed_ids_runs_df
