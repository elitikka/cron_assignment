import streamlit as st 
import requests
import mysql.connector 
import pandas as pd 
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="/home/ubuntu/cron_assignment/.env")

st.title("Oulun sää nyt ja Helsingin säädata")
st.write("Oulu: Norjan ilmatieteenlaitoksen API, Helsinki: OpenWeather API")

# OULU SÄÄ - Norjan ilmatieteenlaitos
# Oulu sijainti
OU_LAT = 65.0121
OU_LON = 25.4651
try:
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={OU_LAT}&lon={OU_LON}"
    headers = {"User-Agent": "LinuxAdministrationUniversityAssignment/1.0"}  # Required by MET.NO
    oulu_response = requests.get(url, headers=headers, timeout=10)
    oulu_data = oulu_response.json()

    # Tämänhetkinen sää
    details = oulu_data["properties"]["timeseries"][0]["data"]["instant"]["details"]
    temp = details["air_temperature"]
    wind = details["wind_speed"]

    st.header('Sää Oulussa nyt') 
    st.write(f"Lämpötila: {temp} °C")
    st.write(f"Tuuli: {wind} m/s")

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

st.header('Säädata Helsingistä') 
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
