
from Orbit import Orbit
from Receiver import Receiver
import numpy as np
import Global

class Satellite:
    def __init__(self, orbit: Orbit, receiver: Receiver):
        self.orbit = orbit
        self.receiver = receiver
        self.register()

    def updatePosition(self):
        self.orbit.updateKeplers()

    def getCartesians(self):
        return self.orbit.getCartesians()

    def register(self):
        self.receiver.registerSatellite(self)

    