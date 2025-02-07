import math
import time
t = time.time()
cos_t = math.cos(t)

while True:
    t = time.time()  # Aktuelle Zeit
    cos_t = math.cos(t * 2 * math.pi)  # Skalierung auf eine Periode von 1 Sekunde
    time.sleep(0.01)  # 100 ms Pause für bessere Lesbarkeit
    result = abs(math.degrees(math.atan(cos_t)) - 90)  # Arkustangens von 1
    print(result)  # Ausgabe in Radiant



def step(self):
    cos_t = math.cos(self.passedTime * 2 * math.pi)
    directionAngle = abs(math.degrees(math.atan(cos_t)) - 90)
    point0 = Point(self.truePosition.phi, self.truePosition.lamda)
    point1 = geodesic(kilometers=(self.velocity* Global.deltaT)/1000.0 ).destination(point0, directionAngle)
    self.truePosition.phi = point1.latitude
    self.truePosition.lamda = point1.longitude
    self.distance = (self.distance + self.velocity * Global.deltaT)
    if self.distance > 50:
        self.counter  = (self.counter + 1) % 4
        self.distance = 0