import subprocess

for i in range(1000):
    #print("Starte Simulation...")
    result = subprocess.run(["python", "sim.py"], capture_output=True, text=True)
    
    # Ergebnis anzeigen
    if result.stdout.strip() != "":
        #print("Simulationsausgabe:", result.stdout.strip())  
        print(str(result.stdout.strip()) + ", ")  

    # Falls sim.py einen Fehler geworfen hat
    if result.returncode != 0:
        #print("Fehler in sim.py:", result.stderr.strip())
        #print("Fehler")
        pass
