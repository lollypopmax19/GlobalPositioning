import subprocess
import csv
import sys
import Global

# Simulationstyp über Argumente wählen
simulation_type = sys.argv[1] if len(sys.argv) > 1 else "sim"
simulation_script = "sim.py" if simulation_type == "sim" else "sim2.py"

# Sicheres Update von Global.py
with open("Global.py", "r") as global_file:
    global_content = global_file.readlines()

with open("Global.py", "w") as global_file:
    deltaT_found = False
    for line in global_content:
        if line.startswith("deltaT"):
            deltaT = 1 if simulation_type == "sim" else 0.2
            global_file.write(f"deltaT = {deltaT}\n")
            deltaT_found = True
        else:
            global_file.write(line)
    if not deltaT_found:
        print("Warnung: 'deltaT' nicht in Global.py gefunden. Keine Änderung vorgenommen.")

# Berechnung der tatsächlichen Distanz
actual_distance = Global.velocity * Global.evaluationTime

# Sicheres Update der gdopEvaluation-Methode in Receiver.py
with open("Receiver.py", "r") as receiver_file:
    receiver_content = receiver_file.readlines()

with open("Receiver.py", "w") as receiver_file:
    updated = False
    for line in receiver_content:
        if "for r in range(" in line:
            if simulation_type == "sim":
                receiver_file.write("        for r in range(4, 9):\n")  # Range der zur Verfügungstehenden Satelliten
            else:
                receiver_file.write("        for r in range(8, 9):\n")  # Range der zur Verfügungstehenden Satelliten, möglich bis 12
            updated = True
        else:
            receiver_file.write(line)
    if not updated:
        print("Warnung: 'gdopEvaluation' Bereich nicht in Receiver.py gefunden. Keine Änderung vorgenommen.")

# CSV-Datei für die Ergebnisse vorbereiten
output_filename = "simulation_results.csv" if simulation_type == "sim" else "simulation2_results.csv"

with open(output_filename, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow([
        "Simulation", "Iteration", "Estimated Distance", "GDOP", 
        "Deviation", "Actual Distance", "Average Satellites Used"
    ])

    for i in range(50):  # 1000 Durchläufe für Sim und 10 für Sim2 (aufgrund der längeren Laufzeit)
        result = subprocess.run(["python", simulation_script], capture_output=True, text=True)
        
        if result.stderr:
            print(f"Fehler in {simulation_script} (Iteration {i + 1}):\n{result.stderr}")
            continue  # Numerische Fehler ignorieren und nächste Iteration starten

        print(f"{simulation_script} Ausgabe (Iteration {i + 1}):")
        output_lines = result.stdout.strip().split('\n')
        for idx, line in enumerate(output_lines):
            print(f"Zeile {idx + 1}: {line}")  # Jede Zeile der Ausgabe anzeigen
        
        if result.stdout.strip():
            try:
                # Satellitenanzahl erfassen
                satellite_counts = [int(line.split(": ")[1]) for line in output_lines if "Used Satellites:" in line]
                avg_satellites_used = sum(satellite_counts) / len(satellite_counts) if satellite_counts else 0

                # Nur numerische Zeilen für geschätzte Distanz und GDOP erfassen
                numeric_lines = [line for line in output_lines if line.replace('.', '', 1).isdigit()]
                
                estimated_dist = float(numeric_lines[-1]) if numeric_lines else None
                gdop = float(numeric_lines[-2]) if len(numeric_lines) >= 2 else None

                if estimated_dist is not None:
                    deviation = abs(estimated_dist - actual_distance)
                else:
                    deviation = None
                
                csv_writer.writerow([
                    simulation_type, i + 1, estimated_dist, gdop, 
                    deviation, actual_distance, avg_satellites_used
                ])
            except (IndexError, ValueError) as e:
                print(f"Fehler bei {simulation_script} in Iteration {i + 1}: {e}")