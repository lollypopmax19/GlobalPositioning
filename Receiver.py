
import random
from GeodeticCoords import GeodeticCoords
from CartesianCoords import CartesianCoords
from geopy.distance import geodesic
import Satellite
from geopy.point import Point  #karney formelas
import numpy as np
import Global
import Satellite
import math

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
                #gdop evalutation
                #calc satellite specific noise
                #estimate position with satellites {iterative least square}
                #filtering : kalman small gdop and particle for huge gdop
                #updating self.estimatedPosition
            #}
            sData = self.getSatellitesData()
            fData = self.filterSatelliteDate(sData)


            self.step()
            self.stepSatellites()
            self.passedTime += Global.deltaT

    def gdopEvaluation(self, fData):
        #{
            #teste 4 elementige
            #teste 5 elementige
            #teste 6 elementige
            #teste 7 elementige
        #}
        pass

    def getGeometryMatrix(self, dataSet):
        matrix = []

        receiverX = self.truePosition.getAsCartesianCoords().x  
        receiverY = self.truePosition.getAsCartesianCoords().y   
        receiverZ = self.truePosition.getAsCartesianCoords().z   

        for d in dataSet:
            rho = math.sqrt( (d[0].x - receiverX)**2 + (d[0].y - receiverY)**2 + (d[0].z - receiverZ)**2 )
            row = [ (d[0].x - receiverX) / rho , (d[0].y - receiverY) / rho , (d[0].z - receiverZ) / rho, 1]
            matrix.append(row)

        return matrix

    def filterSatelliteDate(self, sData):
        return [d for d in sData if d[1] < 75.0]

    def getSatellitesData(self):
        satellitesCoords = self.getSatellitesCoords()
        satellitesAngles = self.getSatellitesAngles(satellitesCoords)
        sData = []
        for x in range(len(self.satellites)):
            sData.append( [satellitesCoords[x] , satellitesAngles[x] ] )
        return sData

    def getSatellitesCoords(self):
        coords = []
        for s in self.satellites:
            coords.append( s.getCartesians() )
        return coords

    def getSatellitesAngles(self, coords):
        angles = []
        for s in coords:
            receiverToSat = [s.x - self.truePosition.getAsCartesianCoords().x, s.y - self.truePosition.getAsCartesianCoords().y, s.z - self.truePosition.getAsCartesianCoords().z]
            norm = self.getNormalVectorAtReceiversPosition()
            a = self.getAngleBetweenVectors(receiverToSat, norm)
            angles.append(a)
        return angles

    def stepSatellites(self):
        for s in self.satellites:
            s.updatePosition()

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

    def getNormalVectorAtReceiversPosition(self):
        nx = 2 * self.truePosition.getAsCartesianCoords().x / Global.a_earth **2 
        ny = 2 * self.truePosition.getAsCartesianCoords().y / Global.a_earth **2 
        nz = 2 * self.truePosition.getAsCartesianCoords().z / Global.b_earth **2 
        norm = math.sqrt(nx**2 + ny**2 + nz**2)
        return [nx/norm, ny/norm, nz/norm]

    def getAngleBetweenVectors(self, v1, v2):
        v1 = np.array(v1)
        v2 = np.array(v2)
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        cos_theta = np.clip(dot_product / (norm_v1 * norm_v2), -1.0, 1.0)
        theta = np.degrees(np.arccos(cos_theta))
        return abs(theta)
        
    def registerSatellite(self, sat : Satellite):
        self.satellites.append(sat)

