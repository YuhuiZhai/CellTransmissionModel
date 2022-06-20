from road import Road
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
class Network:
    def __init__(self):
        self.roads = {}
        self.dt = None 
        self.T = None
        self.xrange, self.yrange = (0, 0), (0, 0)
        
    def addRoad(self, road:Road):
        if road.id == None:
            print("id and coordinates are not defined")
            return
        self.dt = road.dt
        self.roads[road.id] = road
        sx, sy, ex, ey = road.sx, road.sy, road.ex, road.ey
        self.xrange = (min(self.xrange[0], sx, ex), max(self.xrange[1], sx, ex))
        self.yrange = (min(self.yrange[0], sy, ey), max(self.yrange[1], sy, ey))        
        

    def connectRoad(self, road1:Road, road2:Road):
        cell1, cell2 = road1.cells[road1.cell_num-1], road2.cells[0]
        cell1.linkNext(cell2)
        road2.gate.blocked = True
        return 

    # function to merge road1 and road2 to road3 
    def mergeRoad(self, road1:Road, road2:Road, road3:Road):
        Bk, Ck, Ek = road1.cells[road1.cell_num-1], road2.cells[road2.cell_num-1], road3.cells[0]
        road1.exit.blocked = True
        road2.exit.blocked = True
        road3.gate.blocked = True
        Bk.linkNext(Ek)
        Ck.linkNext(Ek)
        Bk.status, Ck.status = 1, 1
        Bk.merged_cell = Ck
        Ck.merged_cell = Bk

    def move(self):
        for r in self.roads.values():
            r.move()
        return

    def update(self):
        for r in self.roads.values():
            r.update()
        return 

    def simulate(self, T):   
        for t in np.arange(0, T, self.dt):
            self.move()
            self.update()
        self.T = T
        return 
    
    # request = (id, locs, q, t)
    def addRequest(self, request:tuple):
        id, locs, q, t = request
        self.roads[id].addRequest(locs, q, t) 

    def animation(self):
        print("plotting")
        fig = plt.figure()   
        def animation_func(i):
            plt.clf()
            deltax, deltay = abs(self.xrange[0]-self.xrange[1]), abs(self.yrange[0]-self.yrange[1])
            plt.xlim(self.xrange[0]-1/4*deltax, self.xrange[1]+1/4*deltax)
            plt.ylim(self.yrange[0]-1/4*deltay, self.yrange[1]+1/4*deltay)
            plt.title("Cell transmission model animation")
            plt.xlabel("x")
            plt.ylabel("y")
            for r in self.roads.values():
                curr = r.record[i]
                x, y = [r.cells[idx].position[0] for idx in range(r.cell_num)], [r.cells[idx].position[1] for idx in range(r.cell_num)]
                area = [num**2 for num in curr]
                plt.scatter(x, y, color="red", s=area)
        anim = FuncAnimation(fig, animation_func, frames=int(self.T/self.dt))
        writergif = PillowWriter(15) 
        anim.save("{}road_{}sec.gif".format(len(self.roads), self.dt*3600), writer=writergif)
        print("plot has been saved as {}road_{}sec.gif".format(len(self.roads), self.dt*3600))
        return