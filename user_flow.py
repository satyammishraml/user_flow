import retentioneering
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)


from datetime import datetime, timedelta
import pandas as pd

# load sample data

def make_event_query(date):
    query = """SELECT  timestamp, user_id, entity_type FROM `safalta-294406.sf_dataset.events_views` 
                    WHERE DATE(timestamp)='{}'
                    """.format(date)
    return query


@st.experimental_memo(ttl=600)
def run_query(query):
    query_job = client.query(query)
    data = query_job.to_dataframe()
    return data


retentioneering.config.update({
    'user_col': 'user_id',
    'event_col': 'entity_type',
    'event_time_col': 'timestamp',
})

#user_id = st.text_input('Enter User ID', 'Enter User ID')
today = datetime.today()
tomorrow = today + timedelta(days=10)
start_date = st.date_input('Start date', today)
end_date = st.date_input('End date', tomorrow)
if start_date > end_date:
    st.error('Error: End date must fall after start date.')

start_date = start_date.strftime("%Y-%m-%d")
end_date = end_date.strftime("%Y-%m-%d")
events_views_query = make_event_query(start_date)
df = run_query(events_views_query)

short_df = df[df.entity_type.isin(['course', 'page', 'app-home', 'Safalta', 'blog'])]
data = short_df[['user_id', 'entity_type', 'timestamp']]

st.write(short_df)
retentioneering.config.update({
    'user_col': 'user_id',
    'event_col': 'entity_type',
    'event_time_col': 'timestamp',
})

data.rete.plot_graph(norm_type=None,
                     weight_col=None,
                     thresh=250)
