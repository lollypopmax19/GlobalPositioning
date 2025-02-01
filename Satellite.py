
from Orbit import Orbit

class Satellite:
    def __init__(self, orbit: Orbit):
        self.orbit = orbit

    def updatePosition(self):
        self.orbit.updateKeplers()

    def getCartesians(self):
        return self.orbit.getCartesians()