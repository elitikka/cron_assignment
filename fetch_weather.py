#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
import requests 
import mysql.connector 
from datetime import datetime, timedelta, timezone 
from dotenv import load_dotenv
import os
from fmiopendata.wfs import download_stored_query

# ENV tiedoston salaisuudet
load_dotenv("/home/ubuntu/cron_assignment/.env")

# Suomen Ilmatieteenlaitoksen säätutka
# Jos kuville ei ole kansiota, kansio luodaan
radar_dir = "/home/ubuntu/cron_assignment/fmi_data/radar"
os.makedirs(radar_dir, exist_ok=True)

# DATETIME RANGE: viimeisin tunti UTC
endtime = datetime.now(timezone.utc)
starttime = endtime - timedelta(hours=1)

# muuta formaattia(ISO format with Z)
starttime_iso = starttime.isoformat(timespec='seconds').replace('+00:00', 'Z')
endtime_iso = endtime.isoformat(timespec='seconds').replace('+00:00', 'Z')

try:
    # Lataa tutkakuva komposiitti
    composite = download_stored_query(
        "fmi::radar::composite::dbz",
        starttime=starttime_iso,
        endtime=endtime_iso
        bbox="20,59,32,71,epsg::4326"  # bounding box Suomelle
    )

    # Tallenna kuva
    radar_file = os.path.join(radar_dir, "latest_radar.png")
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