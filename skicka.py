import requests
import os
import time
from datetime import datetime
import json

# ThingSpeak API-konfiguration
THINGSPEAK_API_KEY = "BP48R0EULYT3QVLU"  # Ersätt med din ThingSpeak API-nyckel
THINGSPEAK_URL = "https://api.thingspeak.com/update.json"

# Loggfiler
LOG_DIRECTORY = "/home/ulf/loggfiler/"

# Funktion för att läsa JSON-filer rad för rad och hämta värdena
def read_json_file(file_path):
    try:
        values = []
        with open(file_path, "r") as file:
            for line in file:
                data = json.loads(line.strip())
                values.append(data)
        return values
    except json.JSONDecodeError as e:
        print(f"JSON Error i filen {file_path}: {e}")
        return None
    except Exception as e:
        print(f"Fel vid läsning av filen {file_path}: {e}")
        return None

# Funktion för att skicka loggfiler till ThingSpeak
def send_log_to_thingspeak():
    # Läs data från JSON-loggfiler
    vibration_count_data = read_json_file("/home/ulf/loggfiler/vibration_count_log.json")
    frequency_data = read_json_file("/home/ulf/loggfiler/frequency_log.json")
    amplitude_data = read_json_file("/home/ulf/loggfiler/amplitude_log.json")
    velocity_data = read_json_file("/home/ulf/loggfiler/velocity_log.json")
    
    if vibration_count_data and frequency_data and amplitude_data and velocity_data:
        # Här mappar vi loggdata till rätt fält
        for vibration_count, frequency, amplitude, velocity in zip(vibration_count_data, frequency_data, amplitude_data, velocity_data):
            timestamp = vibration_count["timestamp"]  # Alla har samma tidsstämpel

            payload = {
                "api_key": THINGSPEAK_API_KEY,
                "field1": vibration_count.get("value", ""),
                "field2": frequency.get("value", ""),
                "field3": amplitude.get("value", ""),
                "field4": velocity.get("value", ""),
                "field5": timestamp  # Tidsstämpel (fält 5, om du vill ha det)
            }

            # Skicka till ThingSpeak via HTTP POST
            response = requests.post(THINGSPEAK_URL, data=payload)

            if response.status_code == 200:
                print(f"Skickar loggdata till ThingSpeak...")
            else:
                print(f"Fel vid att skicka loggdata till ThingSpeak: {response.status_code}")
    else:
        print("Någon eller flera loggfiler saknas eller kan inte läsas.")

# Huvudloop för att kontrollera loggfiler och skicka till ThingSpeak
def main():
    try:
        while True:
            # Skicka loggdata till ThingSpeak
            send_log_to_thingspeak()

            # Vänta 15 sekunder innan nästa skickning
            time.sleep(15)

    except KeyboardInterrupt:
        print("Program avslutat.")

# Starta programmet
if __name__ == "__main__":
    main()


