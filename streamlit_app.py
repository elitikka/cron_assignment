import streamlit as st 
import requests
import mysql.connector 
import pandas as pd 
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="/home/ubuntu/cron_assignment/.env")

# OULU SÄÄ
CITY = "Oulu"
try:
    oulu_response = requests.get(f"http://goweather.xyz/weather/{CITY}", timeout=10)
    oulu_data = oulu_response.json()
    st.subheader(f"Sää nyt ({CITY})")
    st.write(f"Lämpötila: {oulu_data['temperature']}")
    st.write(f"Tuuli: {oulu_data['wind']}")
except Exception as e:
    st.error("Säätietoja ei saatavilla")
    st.write(e)


# OPEN WEATHER AVOIN SÄÄDATA + MYSQL
# Avaa yhteys MySQL tietokantaan
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)
# Hae viimeisimmät 50 riviä säädataa
df = pd.read_sql('SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50', 
conn) 
conn.close() # Sulje tietokannan yhteys

# Muuta aikaformaatti
df['timestamp'] = pd.to_datetime(df['timestamp'])

st.title('Säädata Helsingistä') 
fig = px.line(
    df,
    x='timestamp',        # X-axis: timestamp of observation
    y='temperature',      # Y-axis: temperature in Celsius
    labels={'timestamp': 'Time', 'temperature': 'Temperature (°C)'}
)

# Piirrä kuvaaja
st.plotly_chart(fig, use_container_width=True)
# Taulukko
st.dataframe(df)
