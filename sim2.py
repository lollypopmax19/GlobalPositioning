from Orbit import Orbit
from Satellite import Satellite
from Receiver import Receiver
from Tracker import Tracker
import Global
import math

def sim():
    o1a = Orbit(20000000, 0.01, math.radians(60), math.radians(0), math.radians(90), math.radians(0))
    o1b = Orbit(20000000, 0.01, math.radians(60), math.radians(0), math.radians(90), math.radians(60))
    o1c = Orbit(20000000, 0.01, math.radians(60), math.radians(0), math.radians(90), math.radians(120))
    o1d = Orbit(20000000, 0.01, math.radians(60), math.radians(0), math.radians(90), math.radians(180))
    o1e = Orbit(20000000, 0.01, math.radians(60), math.radians(0), math.radians(90), math.radians(240))
    o1f = Orbit(20000000, 0.01, math.radians(60), math.radians(0), math.radians(90), math.radians(300))

    o2a = Orbit(20000000, 0.01, math.radians(60), math.radians(45), math.radians(90), math.radians(0))
    o2b = Orbit(20000000, 0.01, math.radians(60), math.radians(45), math.radians(90), math.radians(60))
    o2c = Orbit(20000000, 0.01, math.radians(60), math.radians(45), math.radians(90), math.radians(120))
    o2d = Orbit(20000000, 0.01, math.radians(60), math.radians(45), math.radians(90), math.radians(180))
    o2e = Orbit(20000000, 0.01, math.radians(60), math.radians(45), math.radians(90), math.radians(240))
    o2f = Orbit(20000000, 0.01, math.radians(60), math.radians(45), math.radians(90), math.radians(300))

    o3a = Orbit(20000000, 0.01, math.radians(60), math.radians(90), math.radians(90), math.radians(0))
    o3b = Orbit(20000000, 0.01, math.radians(60), math.radians(90), math.radians(90), math.radians(60))
    o3c = Orbit(20000000, 0.01, math.radians(60), math.radians(90), math.radians(90), math.radians(120))
    o3d = Orbit(20000000, 0.01, math.radians(60), math.radians(90), math.radians(90), math.radians(180))
    o3e = Orbit(20000000, 0.01, math.radians(60), math.radians(90), math.radians(90), math.radians(240))
    o3f = Orbit(20000000, 0.01, math.radians(60), math.radians(90), math.radians(90), math.radians(300))

    o4a = Orbit(20000000, 0.01, math.radians(60), math.radians(135), math.radians(90), math.radians(0))
    o4b = Orbit(20000000, 0.01, math.radians(60), math.radians(135), math.radians(90), math.radians(60))
    o4c = Orbit(20000000, 0.01, math.radians(60), math.radians(135), math.radians(90), math.radians(120))
    o4d = Orbit(20000000, 0.01, math.radians(60), math.radians(135), math.radians(90), math.radians(180))
    o4e = Orbit(20000000, 0.01, math.radians(60), math.radians(135), math.radians(90), math.radians(240))
    o4f = Orbit(20000000, 0.01, math.radians(60), math.radians(135), math.radians(90), math.radians(300))

    o5a = Orbit(20000000, 0.01, math.radians(60), math.radians(180), math.radians(90), math.radians(0))
    o5b = Orbit(20000000, 0.01, math.radians(60), math.radians(180), math.radians(90), math.radians(60))
    o5c = Orbit(20000000, 0.01, math.radians(60), math.radians(180), math.radians(90), math.radians(120))
    o5d = Orbit(20000000, 0.01, math.radians(60), math.radians(180), math.radians(90), math.radians(180))
    o5e = Orbit(20000000, 0.01, math.radians(60), math.radians(180), math.radians(90), math.radians(240))
    o5f = Orbit(20000000, 0.01, math.radians(60), math.radians(180), math.radians(90), math.radians(300))

    o6a = Orbit(20000000, 0.01, math.radians(60), math.radians(225), math.radians(90), math.radians(0))
    o6b = Orbit(20000000, 0.01, math.radians(60), math.radians(225), math.radians(90), math.radians(60))
    o6c = Orbit(20000000, 0.01, math.radians(60), math.radians(225), math.radians(90), math.radians(120))
    o6d = Orbit(20000000, 0.01, math.radians(60), math.radians(225), math.radians(90), math.radians(180))
    o6e = Orbit(20000000, 0.01, math.radians(60), math.radians(225), math.radians(90), math.radians(240))
    o6f = Orbit(20000000, 0.01, math.radians(60), math.radians(225), math.radians(90), math.radians(300))

    o7a = Orbit(20000000, 0.01, math.radians(60), math.radians(270), math.radians(90), math.radians(0))
    o7b = Orbit(20000000, 0.01, math.radians(60), math.radians(270), math.radians(90), math.radians(60))
    o7c = Orbit(20000000, 0.01, math.radians(60), math.radians(270), math.radians(90), math.radians(120))
    o7d = Orbit(20000000, 0.01, math.radians(60), math.radians(270), math.radians(90), math.radians(180))
    o7e = Orbit(20000000, 0.01, math.radians(60), math.radians(270), math.radians(90), math.radians(240))
    o7f = Orbit(20000000, 0.01, math.radians(60), math.radians(270), math.radians(90), math.radians(300))

    o8a = Orbit(20000000, 0.01, math.radians(60), math.radians(315), math.radians(90), math.radians(0))
    o8b = Orbit(20000000, 0.01, math.radians(60), math.radians(315), math.radians(90), math.radians(60))
    o8c = Orbit(20000000, 0.01, math.radians(60), math.radians(315), math.radians(90), math.radians(120))
    o8d = Orbit(20000000, 0.01, math.radians(60), math.radians(315), math.radians(90), math.radians(180))
    o8e = Orbit(20000000, 0.01, math.radians(60), math.radians(315), math.radians(90), math.radians(240))
    o8f = Orbit(20000000, 0.01, math.radians(60), math.radians(315), math.radians(90), math.radians(300))

    r = Receiver(Global.velocity)
    s1a = Satellite(o1a,r)
    s1b = Satellite(o1b,r)
    s1c = Satellite(o1c,r)
    s1d = Satellite(o1d,r)
    s1e = Satellite(o1e,r)
    s1f = Satellite(o1f,r)

    s2a = Satellite(o2a,r)
    s2b = Satellite(o2b,r)
    s2c = Satellite(o2c,r)
    s2d = Satellite(o2d,r)
    s2e = Satellite(o2e,r)
    s2f = Satellite(o2f,r)

    s3a = Satellite(o3a,r)
    s3b = Satellite(o3b,r)
    s3c = Satellite(o3c,r)
    s3d = Satellite(o3d,r)
    s3e = Satellite(o3e,r)
    s3f = Satellite(o3f,r)

    s4a = Satellite(o4a,r)
    s4b = Satellite(o4b,r)
    s4c = Satellite(o4c,r)
    s4d = Satellite(o4d,r)
    s4e = Satellite(o4e,r)
    s4f = Satellite(o4f,r)

    s5a = Satellite(o5a,r)
    s5b = Satellite(o5b,r)
    s5c = Satellite(o5c,r)
    s5d = Satellite(o5d,r)
    s5e = Satellite(o5e,r)
    s5f = Satellite(o5f,r)

    s6a = Satellite(o6a,r)
    s6b = Satellite(o6b,r)
    s6c = Satellite(o6c,r)
    s6d = Satellite(o6d,r)
    s6e = Satellite(o6e,r)
    s6f = Satellite(o6f,r)

    s7a = Satellite(o7a,r)
    s7b = Satellite(o7b,r)
    s7c = Satellite(o7c,r)
    s7d = Satellite(o7d,r)
    s7e = Satellite(o7e,r)
    s7f = Satellite(o7f,r)

    s8a = Satellite(o8a,r)
    s8b = Satellite(o8b,r)
    s8c = Satellite(o8c,r)
    s8d = Satellite(o8d,r)
    s8e = Satellite(o8e,r)
    s8f = Satellite(o8f,r)

    t = Tracker(r)

    r.run()
    sigma = t.calcDeviation()
    estimatedDist = t.calcEstimatedDistance()
    #t.visualize()  Zur Visualisierung des Weges
    print(t.averageUsedGdop())
    return estimatedDist

if __name__ == "__main__":
    result = sim()
    print(result)