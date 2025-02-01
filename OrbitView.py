import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Orbit import Orbit
from Satellite import Satellite
import Global

satellite_data = [
    {"a": 20000000, "e": 0.01, "i": math.radians(55), "bigOmega": math.radians(0), "smallOmega": math.radians(90), "theta": math.radians(0)},
    {"a": 20000000, "e": 0.01, "i": math.radians(55), "bigOmega": math.radians(60), "smallOmega": math.radians(120), "theta": math.radians(0)},
    {"a": 20000000, "e": 0.01, "i": math.radians(55), "bigOmega": math.radians(120), "smallOmega": math.radians(135), "theta": math.radians(0)}
]

satellites = []
for data in satellite_data:
    orbit = Orbit(data["a"] + Global.a_earth, data["e"], data["i"], data["bigOmega"], data["smallOmega"], data["theta"])
    satellites.append(Satellite(orbit))

deltaT = 10
simulation_duration = 100000 
time_steps = simulation_duration // deltaT

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")
ax.set_title("Satellitenbahnen um die Erde mit WGS84-Ellipsoid")

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
earth_x = Global.a_earth * np.outer(np.cos(u), np.sin(v))
earth_y = Global.a_earth * np.outer(np.sin(u), np.sin(v))
earth_z = Global.b_earth * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(earth_x, earth_y, earth_z, color='blue', alpha=0.5)

satellite_positions = {i: [] for i in range(len(satellites))}

for t in range(time_steps):
    for i, satellite in enumerate(satellites):
        satellite.updatePosition(deltaT)
        x= satellite.getCartesians().x
        y= satellite.getCartesians().y
        z= satellite.getCartesians().z
        satellite_positions[i].append((x, y, z))

for i, positions in satellite_positions.items():
    x_vals, y_vals, z_vals = zip(*positions)
    ax.plot(x_vals, y_vals, z_vals, label=f"Satellit {i+1}")

ax.legend()
plt.show()
