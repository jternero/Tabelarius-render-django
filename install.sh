#!/usr/bin/env bash

# Instalar Google Chrome y ChromeDriver en Render
apt-get update && apt-get install -y wget curl unzip 

# Descargar e instalar Google Chrome
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb 
dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -fy  

# Descargar e instalar ChromeDriver
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1) 
wget -q "https://chromedriver.storage.googleapis.com/$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION)/chromedriver_linux64.zip" 
unzip chromedriver_linux64.zip -d /usr/local/bin/ 
chmod +x /usr/local/bin/chromedriver  

# Instalar dependencias de Python
pip install --no-cache-dir -r requirements.txt  

# Recopilar archivos estáticos de Django
python manage.py collectstatic --noinput  
