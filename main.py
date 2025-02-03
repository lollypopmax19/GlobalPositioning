from Orbit import Orbit
from Satellite import Satellite
from Receiver import Receiver
from Tracker import Tracker
import math

o1a = Orbit(20000000, 0.01, math.radians(55), math.radians(0), math.radians(90), math.radians(0))
o1b = Orbit(20000000, 0.01, math.radians(55), math.radians(0), math.radians(90), math.radians(90))
o1c = Orbit(20000000, 0.01, math.radians(55), math.radians(0), math.radians(90), math.radians(180))
o1d = Orbit(20000000, 0.01, math.radians(55), math.radians(0), math.radians(90), math.radians(270))

o2a = Orbit(20000000, 0.01, math.radians(55), math.radians(60), math.radians(90), math.radians(0))
o2b = Orbit(20000000, 0.01, math.radians(55), math.radians(60), math.radians(90), math.radians(90))
o2c = Orbit(20000000, 0.01, math.radians(55), math.radians(60), math.radians(90), math.radians(180))
o2d = Orbit(20000000, 0.01, math.radians(55), math.radians(60), math.radians(90), math.radians(270))

o3a = Orbit(20000000, 0.01, math.radians(55), math.radians(120), math.radians(90), math.radians(0))
o3b = Orbit(20000000, 0.01, math.radians(55), math.radians(120), math.radians(90), math.radians(90))
o3c = Orbit(20000000, 0.01, math.radians(55), math.radians(120), math.radians(90), math.radians(180))
o3d = Orbit(20000000, 0.01, math.radians(55), math.radians(120), math.radians(90), math.radians(270))

o4a = Orbit(20000000, 0.01, math.radians(55), math.radians(180), math.radians(90), math.radians(0))
o4b = Orbit(20000000, 0.01, math.radians(55), math.radians(180), math.radians(90), math.radians(90))
o4c = Orbit(20000000, 0.01, math.radians(55), math.radians(180), math.radians(90), math.radians(180))
o4d = Orbit(20000000, 0.01, math.radians(55), math.radians(180), math.radians(90), math.radians(270))

o5a = Orbit(20000000, 0.01, math.radians(55), math.radians(240), math.radians(90), math.radians(0))
o5b = Orbit(20000000, 0.01, math.radians(55), math.radians(240), math.radians(90), math.radians(90))
o5c = Orbit(20000000, 0.01, math.radians(55), math.radians(240), math.radians(90), math.radians(180))
o5d = Orbit(20000000, 0.01, math.radians(55), math.radians(240), math.radians(90), math.radians(270))

o6a = Orbit(20000000, 0.01, math.radians(55), math.radians(300), math.radians(90), math.radians(0))
o6b = Orbit(20000000, 0.01, math.radians(55), math.radians(300), math.radians(90), math.radians(90))
o6c = Orbit(20000000, 0.01, math.radians(55), math.radians(300), math.radians(90), math.radians(180))
o6d = Orbit(20000000, 0.01, math.radians(55), math.radians(300), math.radians(90), math.radians(270))

r = Receiver(3.3)
s1a = Satellite(o1a,r)
s1b = Satellite(o1b,r)
s1c = Satellite(o1c,r)
s1d = Satellite(o1d,r)

s2a = Satellite(o2a,r)
s2b = Satellite(o2b,r)
s2c = Satellite(o2c,r)
s2d = Satellite(o2d,r)

s3a = Satellite(o3a,r)
s3b = Satellite(o3b,r)
s3c = Satellite(o3c,r)
s3d = Satellite(o3d,r)

s4a = Satellite(o4a,r)
s4b = Satellite(o4b,r)
s4c = Satellite(o4c,r)
s4d = Satellite(o4d,r)

s5a = Satellite(o5a,r)
s5b = Satellite(o5b,r)
s5c = Satellite(o5c,r)
s5d = Satellite(o5d,r)

s6a = Satellite(o6a,r)
s6b = Satellite(o6b,r)
s6c = Satellite(o6c,r)
s6d = Satellite(o6d,r)


t = Tracker(r)

r.run()
