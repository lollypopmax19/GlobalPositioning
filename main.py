from Orbit import Orbit
from Satellite import Satellite
from Receiver import Receiver
import math

o = Orbit(20000000, 0.01, math.radians(55), math.radians(0), math.radians(90), math.radians(0))
r = Receiver(30)
s = Satellite(o,r)
n = s.getNoise()

for i in range(100):
    r.truePosition.print()
    r.step()
