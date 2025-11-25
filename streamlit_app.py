import streamlit as st 
import mysql.connector 
import pandas as pd 
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="/home/ubuntu/cron_assignment/.env")

#SUOMEN ILMATIETEENLAITOKSEN AVOIN DATA
# Näytä viimeisin FMI tutkakuva
radar_dir = "/home/ubuntu/cron_assignment/fmi_data/radar"
# Tarkista, onko kansio olemassa. Jos kansiota ei ole olemassa, kansio luodaan.
if os.path.exists(radar_dir) and len(os.listdir(radar_dir)) > 0:
    # Hae viimeisin tutkakuva    
    latest_file = max([os.path.join(radar_dir, f) for f in os.listdir(radar_dir)], key=os.path.getctime)
    # Näytä viimeisin tutkakuva
    st.image(latest_file, caption="Viimeisin tutkakuva (tutkaheijastavuustekijä dBZ)")

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
