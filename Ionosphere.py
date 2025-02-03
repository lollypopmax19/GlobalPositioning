import math

class Ionosphere:
    R_E = 6371
    h1 = 80     
    h2 = 1000 

    @staticmethod
    def traveledDistance(theta):
        theta = math.radians(theta)
        R1 = Ionosphere.R_E + Ionosphere.h1  
        R2 = Ionosphere.R_E + Ionosphere.h2  
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)
        def solve_for_s(R):
            a = 1
            b = -2 * Ionosphere.R_E * cos_theta
            c = Ionosphere.R_E**2 - R**2
            discriminant = b**2 - 4 * a * c
            if discriminant < 0:
                return None 
            s1 = (-b + math.sqrt(discriminant)) / (2 * a)
            s2 = (-b - math.sqrt(discriminant)) / (2 * a)
            return max(s1, s2)
        s1 = solve_for_s(R1)  
        s2 = solve_for_s(R2)  
        if s1 is None or s2 is None:
            return 0.0 
        return abs(s2 - s1) 

    @staticmethod
    def getReference(angle):
        refAngle = 52.5
        refDist = Ionosphere.traveledDistance(refAngle)
        dist = Ionosphere.traveledDistance(angle)
        return dist/refDist


