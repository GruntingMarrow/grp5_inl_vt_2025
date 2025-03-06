  GNU nano 7.2                                                                         ds1302.py                                                                                  
import RPi.GPIO as GPIO
import time
import ntplib
from datetime import datetime
import os

# Definiera GPIO-pinnar
CLK_PIN = 3   # GPIO3 (SCL)
DAT_PIN = 2   # GPIO2 (SDA)
RST_PIN = 4   # GPIO4 (CE)

# Stäng av GPIO-varningar
GPIO.setwarnings(False)

# Initialisera GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK_PIN, GPIO.OUT)
GPIO.setup(DAT_PIN, GPIO.OUT)
GPIO.setup(RST_PIN, GPIO.OUT)

# Funktion för att skriva en byte till DS1302
def write_byte(data):
    for i in range(8):
        GPIO.output(DAT_PIN, (data >> (7 - i)) & 1)
        GPIO.output(CLK_PIN, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(CLK_PIN, GPIO.LOW)
        time.sleep(0.001)

# Funktion för att läsa en byte från DS1302
def read_byte():
    data = 0
    GPIO.output(RST_PIN, GPIO.LOW)  # Låg nivå för att aktivera DS1302
    for i in range(8):
        GPIO.output(CLK_PIN, GPIO.HIGH)
        if GPIO.input(DAT_PIN):
            data |= (1 << (7 - i))
        GPIO.output(CLK_PIN, GPIO.LOW)
        time.sleep(0.001)
    GPIO.output(RST_PIN, GPIO.HIGH)  # Hög nivå för att avsluta kommunikationen
    return data

# Funktion för att skriva till DS1302 (sekunder, minuter, timmar, osv.)
def write_ds1302(address, data):
    GPIO.output(RST_PIN, GPIO.LOW)  # Låg nivå för att aktivera DS1302
    write_byte(address)
    write_byte(data)
    GPIO.output(RST_PIN, GPIO.HIGH)  # Hög nivå för att avsluta kommunikationen

# Funktion för att ställa in tiden på DS1302 från NTP-tid
def set_time_from_ntp():
    # Hämta aktuell tid från NTP-server
    c = ntplib.NTPClient()
    try:
        response = c.request('pool.ntp.org', version=3)
        ntp_time = datetime.utcfromtimestamp(response.tx_time)  # UTC-tid
        print(f"NTP Time: {ntp_time}")  # Skriv ut den mottagna NTP-tiden

        # Extrahera tid och datum från NTP-respons
        year = ntp_time.year - 2000  # DS1302 använder år som 0–99
        month = ntp_time.month
        day = ntp_time.day
        hour = ntp_time.hour
        minute = ntp_time.minute
        second = ntp_time.second

        # Sätt tiden på DS1302 
        write_ds1302(0x00, second)  # Sekunder
        write_ds1302(0x01, minute)  # Minuter
        write_ds1302(0x02, hour)    # Timmar
        write_ds1302(0x03, day)     # Dagar
        write_ds1302(0x04, month)   # Månader
        write_ds1302(0x05, year)    # År (0–99)

    except Exception as e:
        print(f"Error while fetching NTP time: {e}")

# Funktion för att logga tiden i en fil
def log_time():
    log_file = "/home/ulf/time_log.txt"

    # Kontrollera om loggfilen finns, om inte skapa den
    if not os.path.exists(log_file):
        with open(log_file, "w") as file:
            file.write("")  # Skapa en tom fil om den inte finns
        print("Log file created.")

    # Få aktuell tid
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Logga tiden till fil
    with open(log_file, "a") as file:
        file.write(f"{current_time}\n")

#    print(f"Time logged: {current_time}")

# Funktion för att läsa senaste logg
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

# Ställ in tiden från NTP
set_time_from_ntp()

# Starta en loop för att skriva ut senaste loggade tiden varje sekund
try:
    while True:
        # Läs och logga ny tid om den senaste loggade tiden är äldre än den aktuella tiden
        last_logged_time = read_last_log()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Om senaste loggade tiden är äldre än den aktuella tiden, logga den nya tiden
        if last_logged_time != current_time:
            log_time()

#        print(f"Time: {last_logged_time}")  # Skriv ut senaste loggade tiden
        time.sleep(1)  # Vänta i 1 sekund innan nästa utskrift

except KeyboardInterrupt:
    print("Program interrupted. Exiting...")
    GPIO.cleanup()  # Stäng av GPIO vid programavbrott
