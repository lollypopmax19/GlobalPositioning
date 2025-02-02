import math 

class CartesianCoords:
    def __init__(self, x, y, z):
        self.x = x 
        self.y = y 
        self.z = z 

    def print(self):
        print("x: " + str(self.x) + " y: " + str(self.y) + " z: " + str(self.z))

    def getNorm(self):
        return math.sqrt(self.x**2+ self.y**2+ self.z**2)
