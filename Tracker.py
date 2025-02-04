import Global
import math 
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Tracker:
    _receiver = None
    _truePositionCache = []
    _estimatedCache = []
    _gdopCache = []

    def __init__(self, receiver):
        if receiver == None:
            raise ValueError("Receiver is null")
        self._receiver = receiver
        self._receiver.trackRegister(self)

    def updateView(self):
        self._truePositionCache.append([self._receiver.truePosition.getAsCartesianCoords().x , self._receiver.truePosition.getAsCartesianCoords().y, \
        self._receiver.truePosition.getAsCartesianCoords().z])
        self._estimatedCache.append(self._receiver.estimatedPosition)
        self._gdopCache.append(self._receiver.gdop)

    def calcDeviation(self):
        sum = 0
        for entry in range(len(self._truePositionCache)):
            err = self.calcError(entry)
            err = err ** 2
            sum += err
        nSum = sum / len(self._truePositionCache)
        return math.sqrt(nSum)

    def calcError(self, entry):
        true = np.array([self._truePositionCache[entry][0], self._truePositionCache[entry][1], self._truePositionCache[entry][2]])
        est = np.array([self._estimatedCache[entry][0], self._estimatedCache[entry][1], self._estimatedCache[entry][2]])
        error = np.linalg.norm(true - est)
        return error

    def calcEstimatedDistance(self):
        return self.calculatePolygonLength(self._estimatedCache)

    def calculatePolygonLength(self, points):
        length = 0.0
        for i in range(1, len(points)):
            x1, y1, z1 = points[i - 1]
            x2, y2, z2 = points[i]
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
            length += distance
        return length

    def averageUsedGdop(self):
        return sum(self._gdopCache) / len(self._gdopCache)

    def visualize(self):
        self.plot3dPolylines(self._truePositionCache, self._estimatedCache)

    def plot3dPolylines(self, polyline1, polyline2):
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        polyline1 = np.array(polyline1)
        x1, y1, z1 = polyline1[:, 0], polyline1[:, 1], polyline1[:, 2]
        polyline2 = np.array(polyline2)
        x2, y2, z2 = polyline2[:, 0], polyline2[:, 1], polyline2[:, 2]
        ax.plot(x1, y1, z1, label="Polygonzug 1", color="blue", marker="o")
        ax.plot(x2, y2, z2, label="Polygonzug 2", color="red", marker="s")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("3D-Polygonzüge")
        ax.legend()
        plt.show()