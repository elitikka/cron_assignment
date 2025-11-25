import streamlit as st 
import mysql.connector 
import pandas as pd 
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="/home/ubuntu/cron_assignment/.env")

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)
df = pd.read_sql('SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50', 
conn) 
conn.close() 

st.title('Säädata Helsingistä') 
st.dataframe(df) 
