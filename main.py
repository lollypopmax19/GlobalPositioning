
from Satellite import Satellite
from Receiver import Receiver


r = Receiver(30)

for i in range(100):
    r.truePosition.print()
    r.step()
