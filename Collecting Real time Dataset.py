import requests
import pandas as pd
from datetime import datetime
import os
import time
import schedule

API_KEY = '44c539906bac3c7b231df487eee7bf2d'
n = (int)(input("Enter number of cities data: "))
CITIES = []
for i in range(0, n, 1):
    a = (str)(input("Enter city name :"))
    CITIES.append(a)

FILE = r"C:\Users\skj_h\OneDrive\Desktop\SmartWeatherPal Your AI Weather Companion\data.csv"

def fetch_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'city': data['name'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed']
        }
    else:
        print(f"⚠️ Failed to fetch weather for {city}: {response.json().get('message', 'Unknown error')}")
        return None

def collect_data():
    print(f"\n🕒 Collecting weather at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    records = []
    for city in CITIES:
        weather = fetch_weather(city)
        if weather:
            records.append(weather)
            print(f"✅ {city}: {weather['temperature']}°C, {weather['description']}")

    if records:
        df = pd.DataFrame(records)
        if os.path.exists(FILE):
            existing = pd.read_csv(FILE)
            combined = pd.concat([existing, df], ignore_index=True)
        else:
            combined = df

        combined.to_csv(FILE, index=False)
        print("📁 Data saved.\n")
    else:
        print("⚠️ No data saved this round.\n")

# Schedule to run every 10 minutes
schedule.every(1).minutes.do(collect_data)

print("📡 Starting SmartWeatherPal Auto Collector (every 1 min)... Press Ctrl+C to stop.")
collect_data()  # Initial immediate run
while True:
    schedule.run_pending()
    time.sleep(1)
