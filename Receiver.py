
import random
from GeodeticCoords import GeodeticCoords
from CartesianCoords import CartesianCoords
from geopy.distance import geodesic
from geopy.point import Point  #karney formelas
import Global
import Satellite

class Receiver:
    counter = 0
    distance = 0
    passedTime = 0.0

    satellites = []

    def __init__(self, velocity):
        self.truePosition = GeodeticCoords(0,0)
        self.estimatedPosition = CartesianCoords(0,0,0)
        self.spawn()
        self.velocity = velocity

    def spawn(self):
        phi = random.uniform(-90 + 23.5, 90 - 23.5)
        lamda = random.uniform(-180, 180)
        self.truePosition.phi = phi
        self.truePosition.lamda = lamda

    def run(self):
        while self.passedTime < Global.evaluationTime:
            #{
                #get satellites coords
                #calculate satellites angle
                #select possible satellites
                #gdop evalutation
                #calc satellite specific noise
                #estimate position with satellites {iterative least square}
                #filtering : kalman small gdop and particle for huge gdop
                #updating self.estimatedPosition
            #}
            self.passedTime += Global.deltaT

    def step(self):
        destination = 0
        if self.counter == 0:
            destination = 180
        elif self.counter == 1:
            destination = 90
        elif self.counter == 2:
            destination = 0
        else:
            destination = 90

        point0 = Point(self.truePosition.phi, self.truePosition.lamda)
        point1 = geodesic(kilometers=self.velocity/1000.0 * Global.deltaT).destination(point0, destination)
        self.truePosition.phi = point1.latitude
        self.truePosition.lamda = point1.longitude
        self.distance = (self.distance + self.velocity * Global.deltaT)
        if self.distance > 50:
            self.counter  = (self.counter + 1) % 4
            self.distance = 0

    def getSatelliteSpecificNoise(self):
       return np.random.normal(0, Global.sigmaI) + np.random.normal(0, Global.sigmaS) + np.random.normal(0, Global.sigmaU) + np.random.normal(0, Global.sigmaM) \
       + np.random.normal(0, Global.sigmaT) + np.random.normal(0, Global.sigmaR)
        
    def registerSatellite(self, sat : Satellite):
        self.satellites.append(sat)

