import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta
import os

# Definiera GPIO-pinne för Linetracker
LINETRACKER_PIN = 17  # GPIO17

# Stäng av GPIO-varningar
GPIO.setwarnings(False)

# Initialisera GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LINETRACKER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Anta att pinnen är i "pull-up" läge

# Funktion för att läsa senaste logg från time_log.txt
def read_last_log():
    log_file = "/home/ulf/time_log.txt"
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as file:
                lines = file.readlines()
                if lines:
                    last_line = lines[-1]
                    return last_line.strip()  # Returnera senaste loggade tiden
                else:
                    return "No logs found."
        except FileNotFoundError:
            return "Log file not found."
    else:
        return "Log file does not exist."

# Funktion för att logga utlösningar från Linetracker
def log_linetracker_event():
    log_file = "/home/ulf/lintracker.txt"
    
    # Läs den senaste loggade tiden från time_log.txt
    last_logged_time = read_last_log()
    
    if last_logged_time == "No logs found." or last_logged_time == "Log file does not exist.":
        print("Error: Could not read the time_log.txt file.")
        return

    # Få aktuell tid när händelsen inträffar
    event_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Skriv loggen till filen
    with open(log_file, "a") as file:
        file.write(f"{event_time} - Linetracker triggered. Last logged time: {last_logged_time}\n")
    print(f"Event logged: {event_time} - Linetracker triggered.")

# Funktion för att rensa loggen efter 24 timmar
def clear_log_if_needed():
    log_file = "/home/ulf/lintracker.txt"
    
    # Kontrollera om loggen finns och om den är äldre än 24 timmar
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as file:
                lines = file.readlines()
                
                if lines:
                    first_log_time_str = lines[0].split(" - ")[0]
                    first_log_time = datetime.strptime(first_log_time_str, '%Y-%m-%d %H:%M:%S')
                    current_time = datetime.now()

                    # Rensa loggen om den är äldre än 24 timmar
                    if (current_time - first_log_time) > timedelta(hours=24):
                        with open(log_file, "w") as file:
                            file.write("")  # Rensa loggen
                        print("Log file cleared due to 24-hour expiration.")
        except Exception as e:
            print(f"Error while checking log file: {e}")

# Huvudloop för att upptäcka Linetracker-utlösningar
try:
    print("Linetracker Monitoring Started...")
    while True:
        # Kontrollera om pinnen har detekterat en linje (utlösning)
        if GPIO.input(LINETRACKER_PIN) == GPIO.LOW:  # Antag att LOW betyder detektering
            log_linetracker_event()
            time.sleep(1)  # Vänta en sekund innan nästa kontroll för att undvika dubbla loggningar

        clear_log_if_needed()  # Kontrollera om loggen behöver rensas varje gång

except KeyboardInterrupt:
    print("Program interrupted. Exiting...")
    GPIO.cleanup()  # Stäng av GPIO vid programavbrott

   # Få aktuell tid när händelsen inträffar
    event_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Skriv loggen till filen
    with open(log_file, "a") as file:
        file.write(f"{event_time} - Linetracker triggered. Last logged time: {last_logged_time}\n")
    print(f"Event logged: {event_time} - Linetracker triggered.")

# Funktion för att rensa loggen efter 24 timmar
def clear_log_if_needed():
    log_file = "/home/ulf/lintracker.txt"
    
    # Kontrollera om loggen finns och om den är äldre än 24 timmar
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as file:
                lines = file.readlines()

                if lines:
                    first_log_time_str = lines[0].split(" - ")[0]
                    first_log_time = datetime.strptime(first_log_time_str, '%Y-%m-%d %H:%M:%S')
                    current_time = datetime.now()

                    # Rensa loggen om den är äldre än 24 timmar
                    if (current_time - first_log_time) > timedelta(hours=24):
                        with open(log_file, "w") as file:
                            file.write("")  # Rensa loggen
                        print("Log file cleared due to 24-hour expiration.")
        except Exception as e:
            print(f"Error while checking log file: {e}")

# Huvudloop för att upptäcka Linetracker-utlösningar
try:
    print("Linetracker Monitoring Started...")
    while True:
        # Kontrollera om pinnen har detekterat en linje (utlösning)
        if GPIO.input(LINETRACKER_PIN) == GPIO.HIGH:  # Antag att HIGH betyder detektering
            log_linetracker_event()
            time.sleep(1)  # Vänta en sekund innan nästa kontroll för att undvika dubbla loggningar

        clear_log_if_needed()  # Kontrollera om loggen behöver rensas varje gång

except KeyboardInterrupt:
    print("Program interrupted. Exiting...")
    GPIO.cleanup()  # Stäng av GPIO vid programavbrott
