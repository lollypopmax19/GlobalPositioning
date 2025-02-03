import subprocess
import csv

# CSV-Datei zum Schreiben öffnen
with open("simulation_output.csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Simulation Output"])  # Kopfzeile schreiben
    
    for i in range(5000):
        result = subprocess.run(["python", "sim.py"], capture_output=True, text=True)
        
        if result.stdout.strip() != "":
            output = result.stdout.strip()
            print(output + ", ")
            csv_writer.writerow([output])  # Ausgabe in die CSV-Datei schreiben
        
        if result.returncode != 0:

            pass  # Falls sim.py einen Fehler wirft
