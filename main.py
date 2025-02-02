from Orbit import Orbit
from Satellite import Satellite
from Receiver import Receiver
import math

o = Orbit(20000000, 0.01, math.radians(55), math.radians(0), math.radians(90), math.radians(0))
r = Receiver(3.3)
s1 = Satellite(o,r)
s2 = Satellite(o,r)
s3 = Satellite(o,r)

for i in range(100):
    r.truePosition.print()
    r.step()
