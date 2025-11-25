#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
import requests 
import mysql.connector 
from datetime import datetime, timedelta 
from dotenv import load_dotenv
import os
from fmiopendata.wfs import download_stored_query

# ENV tiedoston salaisuudet
load_dotenv("/home/ubuntu/cron_assignment/.env")

# Suomen Ilmatieteenlaitoksen säätutka
radar_dir = "/home/ubuntu/cron_assignment/fmi_data/radar"
os.makedirs(radar_dir, exist_ok=True)

# Määritä datan range: viimeisin tunti (UTC)
endtime = datetime.utcnow()
starttime = endtime - timedelta(hours=1)

try:
    # Lataa viimeisin heijastavuuskomposiitti
    composite = download_stored_query(
        "fmi::radar::composite::dbz",
        starttime=starttime,
        endtime=endtime
    )

    # Tallenna tutkakuva PNG:nä
    radar_file = os.path.join(radar_dir, "latest_radar.png")
    # 'composite.data' is a dict: key=timestamp, value=RadarImage object
    first_image = list(composite.data.values())[0]
    first_image.save_file(radar_file)

    print(f"Latest radar image saved to {radar_file}")
except Exception as e:
    print(f"FMI radar download failed: {e}")


# Open Weather API
OWAPI_KEY = os.getenv("OW_API_KEY")
CITY = 'Helsinki' 
URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OWAPI_KEY}&units=metric' 

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")) 

cursor = conn.cursor() 
cursor.execute('''CREATE TABLE IF NOT EXISTS weather_data (id INT AUTO_INCREMENT PRIMARY KEY, city VARCHAR(50), temperature FLOAT, description VARCHAR(100), timestamp DATETIME)''') 

response = requests.get(URL) 
data = response.json() 
temp = data['main']['temp'] 
desc = data['weather'][0]['description'] 
timestamp = datetime.now() 

cursor.execute('INSERT INTO weather_data (city, temperature, description, timestamp) VALUES (%s, %s, %s, %s)', (CITY, temp, desc, timestamp)) 

conn.commit() 
cursor.close() 
conn.close() 
print(f'Data tallennettu: {CITY} {temp}°C {desc}')