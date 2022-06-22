# Cell Transmission Model
## class Cell
1. The basic class of the simulation. User can ignore it. 

## class Road
1. class Road is the combination of cell. 
2. To define a road, user should enter the required parameter. 

    Example: 

        r0 = Road(id=0, length=1.5, dt=6/3600, v=60, w=60, qinit=2400, qmax=3000, kj=180)
    where `id` is the id, `length` is the total length of the road (dist), `dt` is the time resolution (hr), v is the free velocity (dist/hr), `w` is the backwave velocity (dist/hr), `qini`t is the initial flow in each cell (unit/hr), `qmax` is the maximum flow in each cell (unit/hr), `kj` is the jam density (unit/dist), weight is the inverse of priority (user can ignore this if road is not in a network)

3. After defining a road, it is optional for user to add some accidents or events to change the flow at some locations. If needed, user can use `addRequest()` function. 
    
    Example: We use the same road with length 1.5 km in part 2, at t = 0, there is an accident and the flow at 0.5 km and 1 km are reduced to 0. at t = 5/60 hr, the flow at 1 km is restored to maximum flow.  

        # add accidents
        r0.addRequest(locs=[[0.5, 1], [1]], q=[0, 3000], t=[0, 5/60])

    where `locs` is the list of locations flow changed, `q` is the list of flow changed to, `t` is the list of time flow changed.

4. To simulate, use the function of `simulation()`. 

    Example:

        # do simulation 
        r0.simulate(T=1)
        
    where `T` is the time duration of simulation.

5. After simulation is finished, user can use multiple ways to present the result. User can choose to print the simulation reuslt in terminal using `print()`, export the result to a xlsx file using `export()`, or make animation using `animation()`. 

    Example:

        # print out in terminal
        r0.print()
        
        # export to xlsx
        r0.export(name="text")
        
        # make animation
        r0.animation(type=0)
        r0.animation(type=1)

    where `type` is the animation type. User can decide to animate type 0 or type 1. 

## class Network

1. class Network is the combination of class Road.

2. User can decide to merge or diverge road.   

    Example: 

        # define five roads
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
    
    where `defineLocation(o, d)` function is to define the start point and end point of road. Also the weight should be also defined. Otherwise, it is assumed that all roads have the same priority. 

        # create network 
        n = Network()

        # add fivehree roads to network
        n.addRoad(r0)
        n.addRoad(r1)
        n.addRoad(r2)
        n.addRoad(r3)
        n.addRoad(r4)

        # merge r0 and r1, connected to r2
        n.mergeRoad(r0, r1, r2)
        
        # diverge r2 to {r3 and r4}
        n.divergeRoad(r2, {r3, r4})

        n.simulate(T=20/60)
        n.animation()

