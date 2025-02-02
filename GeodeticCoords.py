
from CartesianCoords import CartesianCoords
import math
import Global

class GeodeticCoords:
    def __init__(self, phi, lamda):
        self.phi = phi
        self.lamda = lamda 
        self.n = self.getN() 

    def getAsCartesianCoords(self):
        return CartesianCoords(
            self.getN() * math.cos( math.radians(self.phi) ) * math.cos( math.radians(self.lamda) ),
            self.getN() * math.cos( math.radians(self.phi)) * math.sin(math.radians(self.lamda)),
            self.getN() * (1 - self.getESquare()) * math.sin(math.radians(self.phi))
        )

    def getN(self):
        return Global.a_earth / math.sqrt(1- self.getESquare() * math.pow( math.sin(math.radians(self.phi)),2))

    def getESquare(self):
        return ( math.pow(Global.a_earth, 2) - math.pow(Global.b_earth, 2) ) / math.pow(Global.a_earth, 2)

    def print(self):
        print("phi: " + str(self.phi) + " lamda: " + str(self.lamda) + " N: " + str(self.n))

    def getNorm(self):
        c= self.getAsCartesianCoords()
        return c.getNorm()
