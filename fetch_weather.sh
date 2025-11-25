#!/bin/bash 
# Polku virtuaaliympäristöön 
PROJECT_DIR="/home/ubuntu/cron_assignment"
VENV_DIR="venv" 

cd $PROJECT_DIR || exit 1

# Luo virtuaaliympäristö, jos ei ole olemassa 
if [ ! -d "$VENV_DIR" ]; then 
    echo "Luodaan virtuaaliympäristö..." 
    python3 -m venv $VENV_DIR 
fi 

# Aktivoi virtuaaliympäristö 
source $VENV_DIR/bin/activate 

# Asenna riippuvuudet requirements.txt-tiedostosta 
if [ -f "requirements.txt" ]; then 
    echo "Asennetaan riippuvuudet..." 
    pip install --upgrade pip 
    pip install -r requirements.txt 
else 
    echo "requirements.txt ei löytynyt!" 
fi 

# Suorita fetch_weather.py 
if [ -f "fetch_weather.py" ]; then 
    echo "Suoritetaan fetch_weather.py..." 
    python fetch_weather.py 
else 
    echo "fetch_weather.py ei löytynyt!" 
fi 
    echo "Valmis!" 