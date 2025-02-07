import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# CSV-Datei laden
simulation_file = "results/simulation_results-Sinus-10kmh.csv" 

df = pd.read_csv(simulation_file)

# Umwandlung in sinnvolle Einheiten
iterations = df["Iteration"]
estimated_distance = df["Estimated Distance"]
actual_distance = df["Actual Distance"]
gdop_values = df["GDOP"]

# Entferne Werte mit einer Abweichung von mehr als 40%
deviation = abs(estimated_distance - actual_distance) / actual_distance
filtered_df = df[deviation <= 0.4]

# Aktualisierte Werte nach dem Filtern
iterations = filtered_df["Iteration"]
estimated_distance = filtered_df["Estimated Distance"]
actual_distance = filtered_df["Actual Distance"]
gdop_values = filtered_df["GDOP"]

# Berechnung des geometrischen Mittels der geschätzten Distanzen
if len(estimated_distance) > 0:
    geometric_mean = np.exp(np.mean(np.log(estimated_distance[estimated_distance > 0])))
    geometric_mean_series = [geometric_mean] * len(iterations)
else:
    geometric_mean_series = [0] * len(iterations)

# Plot erstellen
plt.figure(figsize=(12, 6))

# Tatsächlicher vs. geschätzter Weg
plt.subplot(2, 1, 1)
plt.plot(iterations, actual_distance, label="Tatsächlicher Weg", linestyle='-', marker='o', color='blue')
plt.plot(iterations, estimated_distance, label="Geschätzter Weg", linestyle='--', marker='s', color='red')
plt.plot(iterations, geometric_mean_series, label="Geometrisches Mittel", linestyle=':', color='green')
plt.xlabel("Iteration")
plt.ylabel("Distanz (m)")
plt.legend()
plt.title("Tatsächlicher vs. Geschätzter Weg")

# Skalierung der Y-Achse anhand der geschätzten Distanz
if len(estimated_distance) > 0:
    plt.ylim(min(estimated_distance) * 0.95, max(estimated_distance) * 1.05)

# GDOP-Werte
plt.subplot(2, 1, 2)
plt.plot(iterations, gdop_values, label="GDOP", linestyle='-', marker='x', color='purple')
plt.xlabel("Iteration")
plt.ylabel("GDOP-Wert")
plt.legend()
plt.title("GDOP-Werte über Iterationen")

plt.tight_layout()
plt.show()
