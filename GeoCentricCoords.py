
from CartesianCoords import CartesianCoords
import math
import Global

class GeoCentricCoords:
    def __init__(self, phi, lamda):
        self.phi = phi
        self.lamda = lamda 
        self.n = self.getN() 

    def getAsCartesianCoords(self):
        return CartesianCoords(
            self.getN() * math.cos(self.phi) * math.cos(self.lamda),
            self.getN() * math.cos(self.phi) * math.sin(self.lamda),
            self.getN() * (1 - self.getESquare()) * math.sin(self.phi)
        )

    def getN(self):
        return Global.a_earth / math.sqrt(1- self.getESquare() * math.pow( math.sin(self.phi),2))

    def getESquare(self):
        return ( math.pow(Global.a_earth, 2) - math.pow(Global.b_earth, 2) ) / math.pow(Global.a_earth, 2)

    def print(self):
        print("phi: " + str(self.phi) + " lamda: " + str(self.lamda) + " N: " + str(self.n))