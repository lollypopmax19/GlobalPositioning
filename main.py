
from Satellite import Satellite
from Receiver import Receiver


r = Receiver(30)

for i in range(30):
    r.truePosition.print()
    r.step()
