import math 
import Global
from CartesianCoords import CartesianCoords

class Orbit:
    def __init__(self, a, e, i, bigOmega, smallOmega, theta):
        self.a = a
        self.e = e
        self.i = i
        self.bigOmega = bigOmega
        self.smallOmega = smallOmega
        self.theta = theta
        self.h = self.getSpecificAngularMomentum()

    def getKeplers(self):
        return [self.a, self.e, self.i, self.bigOmega, self.smallOmega, self.theta]

    def updateKeplers(self):
        self.theta += self.getThetaDot() * Global.deltaT

    def getThetaDot(self):
        return self.h / math.pow( self.getRadius() , 2)

    def getRadius(self):
        return (  self.a * (1.0 - math.pow(self.e, 2))    /    (1 + self.e * math.cos(self.theta))   )

    def getSpecificAngularMomentum(self):
        return math.sqrt(Global.G * Global.mEarth * self.a * (1.0 - math.pow(self.e, 2)))

    def getCartesians(self):
        r = self.getRadius()
        return CartesianCoords(
        r * (math.cos(self.smallOmega) * math.cos(self.theta + self.bigOmega) - math.sin(self.smallOmega) * math.sin(self.theta + self.bigOmega) * math.cos(self.i)),
        r * (math.sin(self.smallOmega) * math.cos(self.theta + self.bigOmega) + math.cos(self.smallOmega) * math.sin(self.theta + self.bigOmega) * math.cos(self.i)),
        r * (math.sin(self.theta + self.bigOmega) * math.sin(self.i))
        )