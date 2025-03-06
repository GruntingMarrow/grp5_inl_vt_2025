import subprocess
import time
import signal
import sys

# Lista med skript att starta i ordning
scripts = ["ds1302.py", "linetracker.py", "sw-420_vibcount.py", "read-send.py"]

# Håller reda på processerna
processes = []

def stop_all(signum, frame):
    """ Funktion för att stoppa alla processer vid Ctrl + C """
    print("\nAvslutar alla processer...")
    for process in processes:
        process.terminate()  # Försöker stänga processen normalt
    time.sleep(1)  # Väntar en kort stund
    for process in processes:
        process.kill()  # Dödar processen om den inte avslutats
    sys.exit(0)

# Koppla Ctrl + C (SIGINT) till stop_all
signal.signal(signal.SIGINT, stop_all)

# Starta varje skript med en paus på 2 sekunder mellan
for script in scripts:
    print(f"Startar {script}...")
    process = subprocess.Popen(["python3", script])
    processes.append(process)
    time.sleep(2)

print("Alla skript är nu startade! Tryck Ctrl + C för att stoppa.")

# Håller programmet igång
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    stop_all(None, None)  # Anropa stoppfunktionen vid Ctrl + C
