import Global

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
        pass

    def calcError(self):
        pass

    def calcEstimatedDistance(self):
        pass