import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta
import os

# Definiera GPIO-pinne för SW-420 Vibration Sensor
VIBRATION_SENSOR_PIN = 26  # GPIO17
LOG_FILE = "/home/ulf/VSM_log.txt"
TIME_LOG_FILE = "/home/ulf/time_log.txt"

# Stäng av GPIO-varningar
GPIO.setwarnings(False)

# Initialisera GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(VIBRATION_SENSOR_PIN, GPIO.IN)

# Funktion för att läsa senaste logg från time_log.txt
def read_last_log():
    if os.path.exists(TIME_LOG_FILE):
        try:
            with open(TIME_LOG_FILE, "r") as file:
                lines = file.readlines()
                if lines:
                    last_line = lines[-1]
                    return last_line.strip()
                else:
                    return "No logs found."
        except FileNotFoundError:
            return "Log file not found."
    else:
        return "Log file does not exist."

# Funktion för att logga vibrationer
def log_vibration_event():
    last_logged_time = read_last_log()
    if last_logged_time in ["No logs found.", "Log file does not exist."]:
        print("Error: Could not read the time_log.txt file.")
        return
    
    event_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, "a") as file:
        file.write(f"{event_time} - Vibration detected. Last logged time: {last_logged_time}\n")
    print(f"Event logged: {event_time} - Vibration detected.")

# Funktion för att rensa loggen efter 24 timmar
def clear_log_if_needed():
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as file:
                lines = file.readlines()
                if lines:
                    first_log_time_str = lines[0].split(" - ")[0]
                    first_log_time = datetime.strptime(first_log_time_str, '%Y-%m-%d %H:%M:%S')
                    current_time = datetime.now()
                    
                    if (current_time - first_log_time) > timedelta(hours=24):
                        with open(LOG_FILE, "w") as file:
                            file.write("")
                        print("Log file cleared due to 24-hour expiration.")
        except Exception as e:
            print(f"Error while checking log file: {e}")

# Huvudloop för att övervaka vibrationssensorn
try:
    print("Vibration Sensor Monitoring Started...")
    while True:
        if GPIO.input(VIBRATION_SENSOR_PIN) == GPIO.HIGH:  # HIGH vid vibration
            log_vibration_event()
            time.sleep(1)  # Vänta 1 sekund för att undvika dubbla loggningar

        clear_log_if_needed()

except KeyboardInterrupt:
    print("Program interrupted. Exiting...")
    GPIO.cleanup()
