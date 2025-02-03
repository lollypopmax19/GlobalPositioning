
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
import itertools
from pyproj import Proj, Transformer


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
                #filtering : kalman small gdop and particle for huge gdop
                #updating self.estimatedPosition
            #}
            sData = self.getSatellitesData()
            fData = self.filterSatelliteDate(sData)

            if len(fData)<4:
                raise Exception("Bad Data")

            combination = self.gdopEvaluation(fData)
            signals = self.getSimulatedSignals(combination)

            satPositionArary = self.extractSatPositionArray(signals)
            satDistanceArray = self.extractSatDistanceArray(signals)
            satAngleArray = self.extractSatAngleArray(combination)

            weightMatrix = self.getWeightMatrix(satAngleArray)

            self.estimatedPosition = self.trilateration_3d(satPositionArary, satDistanceArray, weightMatrix)
            print("Estimated: " + str(self.estimatedPosition))
            self.truePosition.getAsCartesianCoords().print()
            arr = np.array([self.truePosition.getAsCartesianCoords().x, self.truePosition.getAsCartesianCoords().y, self.truePosition.getAsCartesianCoords().z])
            error = np.linalg.norm(self.estimatedPosition - arr)
            print(error)
            self.step()
            self.stepSatellites()
            self.passedTime += Global.deltaT

    def extractSatAngleArray(self, satData):
        array = []
        for d in satData:
            array.append(d[1])
        return array

    def extractSatPositionArray(self, signals):
        array = []
        for s in signals:
            array.append(np.array([s[0].x, s[0].y, s[0].z]))
        return array

    def extractSatDistanceArray(self, signals):
        array = []
        for s in signals:
            array.append(np.array(s[1]))
        return array

    def getSimulatedSignals(self, comb):
        signalDataSet = []
        for sat in comb:
            noise = self.getSatelliteSpecificNoise(sat[1])
            realDist = self.getRealDistance(sat[0])
            estimatedDist = realDist +  noise
            signalDataSet.append([sat[0], estimatedDist])
        return signalDataSet


    def trilateration_3d(self, satellites, distances, weights, max_iter=100000, tol=1e-6):
        satellites = np.asarray(satellites)
        distances = np.asarray(distances)
        weights = np.asarray(weights)

        if len(satellites) < 4:
            raise ValueError("At least 4 satellites are required")

        mean_cartesian = np.array([
            self.truePosition.getAsCartesianCoords().x,
            self.truePosition.getAsCartesianCoords().y,
            self.truePosition.getAsCartesianCoords().z
        ])

        transformer = Transformer.from_crs("EPSG:4978", "EPSG:4326", always_xy=True)
        lon, lat, _ = transformer.transform(mean_cartesian[0], mean_cartesian[1], mean_cartesian[2])

        transformer_back = Transformer.from_crs("EPSG:4326", "EPSG:4978", always_xy=True)
        receiver = np.array(transformer_back.transform(lon, lat, 0))

        if weights.ndim == 1:
            W = np.diag(weights) 
        else:
            W = weights

        if W.shape != (len(satellites), len(satellites)):
            raise ValueError("Weight matrix must be square and match the number of satellites")

        for _ in range(max_iter):
            R_i = np.linalg.norm(satellites - receiver, axis=1)
            residuals = distances - R_i

            H = np.zeros((len(satellites), 3))
            for i in range(len(satellites)):
                if R_i[i] < 1e-6:
                    raise ValueError(f"Numerical issues can occur")
                H[i, :] = (receiver - satellites[i]) / R_i[i]

            Ht_W = H.T @ W
            delta = np.linalg.inv(Ht_W @ H) @ (Ht_W @ residuals)

            receiver += delta
            if np.linalg.norm(delta) < tol:
                break
        else:
            print("Max Iterations reached!")

        return receiver


    def getRealDistance(self, coords):
        rx = self.truePosition.getAsCartesianCoords().x
        ry = self.truePosition.getAsCartesianCoords().y  
        rz = self.truePosition.getAsCartesianCoords().z   
        sx = coords.x
        sy = coords.y
        sz = coords.z
        p1 = np.array([rx, ry, rz])
        p2 = np.array([sx, sy, sz])
        return np.linalg.norm(p1 - p2)

    def gdopEvaluation(self, fData):
        bestSatellitePositions = [[], float('inf')]
        for r in range(4, 8):
            for combination in itertools.combinations(fData, r):
                matrix = self.getGeometryMatrix(combination)
                gdop = self.getGDOP(matrix)
                if gdop < bestSatellitePositions[1]:
                    bestSatellitePositions = [combination, gdop]
        if bestSatellitePositions[1] > 100:
            raise Exception("Bad Data")

        return bestSatellitePositions[0]

    def getGDOP(self, matrix):
        matrix = np.array(matrix)
        matrix_3d = matrix[:, :3]
        Q = np.cov(matrix_3d, rowvar=False)
        gdop = np.sqrt(np.trace(Q))
        return gdop

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
        point1 = geodesic(kilometers=(self.velocity* Global.deltaT)/1000.0 ).destination(point0, destination)
        self.truePosition.phi = point1.latitude
        self.truePosition.lamda = point1.longitude
        self.distance = (self.distance + self.velocity * Global.deltaT)
        if self.distance > 50:
            self.counter  = (self.counter + 1) % 4
            self.distance = 0

    def getSatelliteSpecificNoise(self, angle):
    #    noise =  np.random.normal(0, Global.sigmaI) + np.random.normal(0, Global.sigmaS) + np.random.normal(0, Global.sigmaU) + np.random.normal(0, Global.sigmaM) \
    #    + np.random.normal(0, Global.sigmaT) + np.random.normal(0, Global.sigmaR)
    #    print("noise: " + str(noise))
    #    return noise
        return np.random.normal(0, 0.01)

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

    def getWeightMatrix(self, angleArray):
        arr = []
        for a in angleArray:
            arr.append(self.getSatelliteWeight(a))
        return np.diag(arr)

    def getSatelliteWeight(self, angle):
        evaluationAngle = math.radians(90 - angle)
        return math.sin(evaluationAngle) ** 2

    def registerSatellite(self, sat : Satellite):
        self.satellites.append(sat)

