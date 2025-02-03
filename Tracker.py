import Global
import math 
import numpy as np

class Tracker:
    _receiver = None
    _truePositionCache = []
    _estimatedCache = []

    def __init__(self, receiver):
        if receiver == None:
            raise ValueError("Receiver is null")
        self._receiver = receiver
        self._receiver.trackRegister(self)

    def updateView(self):
        self._truePositionCache.append([self._receiver.truePosition.getAsCartesianCoords().x , self._receiver.truePosition.getAsCartesianCoords().y, \
        self._receiver.truePosition.getAsCartesianCoords().z])
        self._estimatedCache.append(self._receiver.estimatedPosition)

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
        pass