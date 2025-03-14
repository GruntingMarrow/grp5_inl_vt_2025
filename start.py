import subprocess
import signal
import sys
import time

# Starta de andra skripten som subprocess
def start_scripts():
    # Starta vib_json.py
    vib_process = subprocess.Popen(['python3', 'vib_json.py'])

    # Starta skicka.py
    skicka_process = subprocess.Popen(['python3', 'skicka.py'])

    return vib_process, skicka_process
# Hantera avslutning av processerna
def stop_scripts(vib_process, skicka_process):
    # Skicka signal för att avsluta processerna snyggt
    print("\nAvslutar skript...")
    vib_process.terminate()
    skicka_process.terminate()

    # Vänta på att processerna stängs av ordentligt
    vib_process.wait()
    skicka_process.wait()
    print("Alla processer avslutade.")
# Huvudprogram
def main():
    try:
        # Starta skripten
        vib_process, skicka_process = start_scripts()

        # Håll programmet igång tills CTRL+C trycks
        print("Skripten är igång. Tryck CTRL+C för att avsluta.")
        while True:
            time.sleep(1)  # Vänta 1 sekund för att hålla programmet igång

    except KeyboardInterrupt:
        # Hantera avslutning med CTRL+C
        stop_scripts(vib_process, skicka_process)
        sys.exit(0)  # Avsluta programmet

# Starta huvudfunktionen
if __name__ == "__main__":
    main()
