import subprocess
import csv

with open("simulation_output.csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Simulation Output"]) 
    
    for i in range(100):
        result = subprocess.run(["python", "sim.py"], capture_output=True, text=True)
        
        if result.stdout.strip() != "":
            output = result.stdout.strip()
            print(output + ", ")
            csv_writer.writerow([output])  
        
        if result.returncode != 0:
            pass  
