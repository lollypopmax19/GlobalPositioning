# import pandas as pd                                   #### Hier der Teil ist für Alpha-Intervalle als Grafik anzeigen zu lassen
# import matplotlib.pyplot as plt
# import numpy as np

# # CSV-Datei laden
# simulation_file = "results/simulation2_results-Sinus-10kmh-sim2.csv"   # Oder "simulation2_results.csv" für sim2

# df = pd.read_csv(simulation_file)

# # Umwandlung in sinnvolle Einheiten
# estimated_distance = df["Estimated Distance"]
# actual_distance = df["Actual Distance"]

# # Berechnung der absoluten Abweichungen in Metern
# errors_meters = abs(estimated_distance - actual_distance)

# # Feinere Alpha-Intervalle für bessere Auflösung der obersten Werte
# alpha_levels = np.linspace(99, 50, 50)  # Mehr Punkte zwischen 99.9% und 50%
# alpha_intervals = {}

# for alpha in alpha_levels:
#     threshold = np.percentile(errors_meters, alpha)
#     alpha_intervals[alpha] = threshold

# # Erstellen des Plots
# plt.figure(figsize=(10, 6))
# plt.plot(alpha_levels, [alpha_intervals[a] for a in alpha_levels], marker='o', linestyle='-', color='red')
# plt.xlabel("Alpha-Intervall (%)")
# plt.ylabel("Maximale Abweichung (m)")
# plt.title("Maximale Abweichung in Metern je Alpha-Intervall")
# plt.gca().invert_xaxis()
# plt.grid()
# plt.show()


# Anzeigen der Tabelle
import pandas as pd
import numpy as np
import ace_tools_open as tools

# CSV-Datei laden
simulation_file = "results/simulation_results-10kmh.csv"  # Oder "simulation2_results.csv" für sim2

df = pd.read_csv(simulation_file)

# Umwandlung in sinnvolle Einheiten
estimated_distance = df["Estimated Distance"]
actual_distance = df["Actual Distance"]

# Berechnung der absoluten Abweichungen in Metern
errors_meters = abs(estimated_distance - actual_distance)

# Feinere Alpha-Intervalle für bessere Auflösung der obersten Werte
alpha_levels = np.linspace(99, 50, 50)  # Mehr Punkte zwischen 99% und 50%
alpha_intervals = {}

for alpha in alpha_levels:
    threshold = np.percentile(errors_meters, alpha)
    alpha_intervals[alpha] = threshold

# Erstellen eines DataFrames zur besseren Darstellung
df_alpha_intervals = pd.DataFrame({
    "Alpha-Intervall (%)": list(alpha_intervals.keys()),
    "Maximale Abweichung (m)": list(alpha_intervals.values())
})

# Anzeigen der Tabelle
tools.display_dataframe_to_user(name="Alpha-Intervall Analyse", dataframe=df_alpha_intervals)