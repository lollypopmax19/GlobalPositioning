
from Orbit import Orbit

class Satellite:
    def __init__(self, orbit: Orbit):
        self.orbit = orbit

    def updatePosition(self, deltaT):
        self.orbit.updateKeplers(deltaT)

    def getCartesians(self):
        return self.orbit.getCartesians()