import random
from GeodeticCoords import GeodeticCoords
from CartesianCoords import CartesianCoords
from geopy.distance import geodesic
import Satellite
from geopy.point import Point  # karney formelas
import numpy as np
import Global
import Satellite
import math
import itertools
from pyproj import Proj, Transformer
from Ionosphere import Ionosphere
from Tracker import Tracker

class KalmanFilter:
    def predict(self):
        self.x = np.dot(self.F, self.x)
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q

    def update(self, z):
        y = z - np.dot(self.H, self.x)
        S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        self.x += np.dot(K, y)
        self.P = np.dot(np.eye(len(self.P)) - np.dot(K, self.H), self.P)

class Receiver:
    counter = 0
    distance = 0
    passedTime = 0.0
    satellites = []
    tracker = None

    def __init__(self, velocity):
        self.truePosition = GeodeticCoords(0, 0)
        self.estimatedPosition = CartesianCoords(0, 0, 0)
        self.estimatedPositionWithoutKalman = CartesianCoords(0,0,0)
        
        self.gdop = 0
        self.spawn()
        self.velocity = velocity
        self.init_kalman_filter()

    def init_kalman_filter(self):
        dim_x = 3 
        dim_z = 3 
        self.kf = KalmanFilter()
        cart = self.truePosition.getAsCartesianCoords()
        self.kf.x = np.array([[cart.x], [cart.y], [cart.z]])
        self.kf.P = np.eye(dim_x) * 10
        self.kf.F = np.eye(dim_x)
        self.kf.H = np.eye(dim_z, dim_x)
        self.kf.R = np.eye(dim_z) * 10
        self.kf.Q = np.eye(dim_x)

    def spawn(self):
        phi = random.uniform(-90 + 23.5, 90 - 23.5)
        lamda = random.uniform(-180, 180)
        self.truePosition.phi = phi
        self.truePosition.lamda = lamda

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

    def run(self):
        while self.passedTime < Global.evaluationTime:
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
            self.updateTracker()
            self.step()
            self.stepSatellites()
            self.passedTime += Global.deltaT

    def trilateration_3d(self, satellites, distances, weights, max_iter=1000, tol=1e-6):
        satellites = np.asarray(satellites)
        distances = np.asarray(distances)
        weights = np.asarray(weights)
        if len(satellites) < 4:
            raise Exception("At least 4 satellites are required")

        receiver = np.array([
            self.truePosition.getAsCartesianCoords().x,
            self.truePosition.getAsCartesianCoords().y,
            self.truePosition.getAsCartesianCoords().z
        ])

        if weights.ndim == 1:
            W = np.diag(weights)
        else:
            W = weights

        for _ in range(max_iter):
            R_i = np.linalg.norm(satellites - receiver, axis=1)
            residuals = distances - R_i
            H = np.zeros((len(satellites), 3))
            for i in range(len(satellites)):
                H[i, :] = (receiver - satellites[i]) / R_i[i]
            Ht_W = H.T @ W

            delta = np.linalg.pinv(Ht_W @ H) @ (Ht_W @ residuals)

            receiver += delta
            if np.linalg.norm(delta) < tol:
                break

        self.estimatedPositionWithoutKalman = receiver

        self.kf.predict()
        self.kf.update(receiver.reshape(-1, 1))
        receiver_filtered = self.kf.x.flatten()

        return receiver_filtered

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
        for r in range(4, 9):
            for combination in itertools.combinations(fData, r):
                matrix = self.getGeometryMatrix(combination)
                gdop = self.getGDOP(matrix)
                if gdop < bestSatellitePositions[1]:
                    bestSatellitePositions = [combination, gdop]
        if bestSatellitePositions[1] > 100:
            raise Exception("Bad Data")
        self.gdop = bestSatellitePositions[1]
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
        if Global.PathMode == 0:
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

        elif Global.PathMode == 1:
            cos_t = math.cos(self.passedTime/50.0 * 2 * math.pi)
            directionAngle = abs(math.degrees(math.atan(cos_t)) - 90)
            point0 = Point(self.truePosition.phi, self.truePosition.lamda)
            point1 = geodesic(kilometers=(self.velocity* Global.deltaT)/1000.0 ).destination(point0, directionAngle)
            self.truePosition.phi = point1.latitude
            self.truePosition.lamda = point1.longitude
            self.distance = (self.distance + self.velocity * Global.deltaT)
            if self.distance > 50:
                self.counter  = (self.counter + 1) % 4
                self.distance = 0


    def getSatelliteSpecificNoise(self, angle):
        muliplier = Ionosphere.getReference(angle)
        p = 0.00837893141
        return np.random.normal(0, p * muliplier)

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

    def trackRegister(self, tracker : Tracker):
        self.tracker = tracker

    def updateTracker(self):
        if self.tracker != None:
            self.tracker.updateView()