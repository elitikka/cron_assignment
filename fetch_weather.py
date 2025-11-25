#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
import requests 
import mysql.connector 
from datetime import datetime 
from dotenv import load_dotenv
from fmiopendata.radar import get_latest_radar_image
import os

# ENV tiedoston salaisuudet
load_dotenv("/home/ubuntu/cron_assignment/.env")


# Suomen Ilmatieteenlaitoksen säätutka
radar_dir = "/home/ubuntu/cron_assignment/fmi_data/radar"
os.makedirs(radar_dir, exist_ok=True)
image_path = get_latest_radar_image(save_dir=radar_dir, image_type="ref")
print(f"Latest radar image saved to {image_path}")

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