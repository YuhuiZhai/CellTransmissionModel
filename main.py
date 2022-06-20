from road import Road
from network import Network 
r0 = Road(0, length=1.5, dt=6/3600, v=60, w=60, qinit=2400, qmax=3000, kj=180, weight=6)
r0.defineLocation((-1.5/2**(1/2), 1.5/2**(1/2)),(0,0))
r1 = Road(1, length=1.5, dt=6/3600, v=60, w=60, qinit=2400, qmax=3000, kj=180, weight=1)
r1.defineLocation((-1.5/2**(1/2), -1.5/2**(1/2)), (0,0))
r2 = Road(2, length=1.5, dt=6/3600, v=60, w=60, qinit=2400, qmax=5000, kj=180, weight=1)
r2.defineLocation((0,0), (1.5,0))


n = Network()
n.addRoad(r0)
n.addRoad(r1)
n.addRoad(r2)

n.addRequest((0, [[1], [1]], [0, 3000], [0, 5/60]))
# n.addRequest((1, [[1], [1]], [0, 3000], [0, 6/60]))
# n.addRequest((2, [[1], [1]], [0, 3000], [0, 6/60]))

n.mergeRoad(r0, r1, r2)
n.simulate(20/60)
n.animation()
# r0.print()
# print("----")
# r1.print()



# r2 = Road(2, length=3, dt=12/3600, v=60, w=60, qinit=2400, qmax=3000, kj=180)
# r2.addRequest([[2.5], [2.5]], [0, 3000], [0, 6/60])
# r2.simulate(20/60)
# r2.animation(1)
# r2.print()