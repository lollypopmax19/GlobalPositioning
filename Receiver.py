
import random
from GeoCentricCoords import GeoCentricCoords
from CartesianCoords import CartesianCoords



class Receiver:
    def __init__(self):
        self.truePosition = GeoCentricCoords(0,0)
        self.estimatedPosition = CartesianCoords(0,0,0)
        self.spawn()

    def spawn(self):
        phi = random.uniform(23.5, 180 - 23.5)
        lamda = random.uniform(0, 360)
        self.truePosition.phi = phi
        self.truePosition.lamda = lamda

        