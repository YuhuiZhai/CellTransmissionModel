from road import Road
from network import Network 
r0 = Road(0, length=1.5, dt=6/3600, v=60, w=60, qinit=2400, qmax=3000, kj=180, weight=10)
r0.defineLocation((-1.5/2**(1/2), 1.5/2**(1/2)),(0,0))
r1 = Road(1, length=1.5, dt=6/3600, v=60, w=60, qinit=2400, qmax=3000, kj=180, weight=1)
r1.defineLocation((-1.5/2**(1/2), -1.5/2**(1/2)), (0,0))
r2 = Road(2, length=1.5, dt=6/3600, v=60, w=60, qinit=2400, qmax=6000, kj=180, weight=1)
r2.defineLocation((0,0), (1.5,0))
r3 = Road(3, length=2*2**(1/2), dt=6/3600, v=60, w=60, qinit=2400, qmax=6000, kj=180, weight=10)
r3.defineLocation((1.5, 0), (1.5+2, 2))
r4 = Road(4, length=2*2**(1/2), dt=6/3600, v=60, w=60, qinit=2400, qmax=6000, kj=180, weight=1)
r4.defineLocation((1.5, 0), (1.5+2, -2))

n = Network()
n.addRoad(r0)
n.addRoad(r1)
n.addRoad(r2)
n.addRoad(r3)
n.addRoad(r4)

# n.addRequest((0, [[1], [1]], [0, 3000], [0, 5/60]))
# n.addRequest((1, [[1], [1]], [0, 3000], [0, 2/60]))
# n.addRequest((2, [[1], [1]], [0, 3000], [0, 6/60]))

n.mergeRoad(r0, r1, r2)
n.divergeRoad(r2, {r3, r4})
n.simulate(20/60)
n.animation()