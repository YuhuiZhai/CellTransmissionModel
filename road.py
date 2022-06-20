from cell import Cell
import heapq as hq
import numpy as np
import heapq as hq
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

class Road:
    def __init__(self, id, length, dt, v, w, qinit, qmax, kj, weight=0):
        self.id = id
        self.length, self.dt, self.v, self.w, self.qinit, self.qmax, self.kj, self.weight = length, dt, v, w, qinit, qmax, kj, weight
        self.cell_num = int(self.length / (self.dt * self.v))
        self.cell_length = self.length / self.cell_num
        self.cell_capacity = self.w * self.kj * self.dt
        self.ninit, self.Qmax = self.qinit*self.dt, self.qmax*self.dt
        self.gate = Cell('g', self.cell_length, self.ninit, self.Qmax, np.inf)
        self.exit = Cell('e', self.cell_length, self.ninit, self.Qmax, np.inf)
        self.cells = {i:Cell(i, self.cell_length, self.ninit, self.Qmax, self.cell_capacity, self.weight) for i in range(self.cell_num)}
        for cell_id in self.cells:
            if cell_id == self.cell_num-1: continue
            self.cells[cell_id].linkNext(self.cells[cell_id+1])
        self.cells['g'], self.cells['e'] = self.gate, self.exit
        self.gate.linkNext(self.cells[0])
        self.cells[self.cell_num-1].linkNext(self.exit)
        self.record = []
        self.flow_record = []
        self.clock = 0
        self.request_board = []
        
    
    def defineLocation(self, start:tuple, end:tuple):
        self.sx, self.sy = start[0], start[1]
        self.ex, self.ey = end[0], end[1]
        dx, dy = (self.ex - self.sx)/self.cell_num, (self.ey - self.sy)/self.cell_num
        for idx in range(self.cell_num):
            self.cells[idx].position = (self.sx+1/2*dx+idx*dx, self.sy+1/2*dy+idx*dy)
        return  

    # locs[i] is the list of location, q[i] is the flow changed to, t[i] is the time flow changed
    def addRequest(self, locs=[[]], q=[], t=[]):
        for i in range(len(t)):
            request = (locs[i], q[i]*self.dt, t[i]) 
            hq.heappush(self.request_board, (request[2], request))
        return 

    def changeQ(self):
        if len(self.request_board) == 0:
            return 
        first_request = self.request_board[0][1]
        while first_request[2] <= self.clock:
            locs, Q = first_request[0], first_request[1]
            for loc in locs:
                cell_id = int(loc/self.length*self.cell_num)
                self.cells[cell_id].Q = Q
            hq.heappop(self.request_board)
            if len(self.request_board) == 0: return 
            else: first_request = self.request_board[0][1] 
        return 
        
    def move(self):
        self.changeQ()
        self.gate.transferNext()
        for i in range(self.cell_num):
            self.cells[i].transferNext()
        return 

    def update(self):
        flows = [self.cells[i].y_out for i in range(self.cell_num)]
        self.flow_record.append(flows)
        for cell in self.cells.values():
            cell.update()
        nums = [self.cells[i].n for i in range(self.cell_num)]
        self.record.append(nums)
        self.clock += self.dt     
        return nums   

    def simulate(self, T):
        self.record.append([self.cells[i].n for i in range(self.cell_num)])
        for t in np.arange(0, T, self.dt):
            self.move()
            self.update()
        return 

    def print(self):
        # for r in self.record:
        #     frmt = "{:>5}"*len(r)
        #     print(frmt.format(*r))
        for r in self.flow_record:
            frmt = "{:>5}"*len(r)
            print(frmt.format(*r))
        return 
    
    def printinfo(self):
        print("Qmax: {}, cell capaity: {}".format(self.Qmax, self.cell_capacity))
        
    def animation(self, type=0):
        print("plotting")
        fig = plt.figure(figsize=(10,4))   
        def animation_func_0(i):
            plt.clf()
            plt.xlim(0-0.25, self.cell_num)
            plt.ylim(0, self.cell_capacity)
            plt.title("Cell transmission model animation")
            plt.xlabel("Cell idx")
            plt.ylabel("Number of vehicle")
            curr = self.record[i]
            plt.vlines(x = [idx for idx in range(self.cell_num)], 
                       ymin = [0 for num in curr], ymax = [num for num in curr], colors = 'red')
        
        def animation_func_1(i):
            plt.clf()
            plt.xlim(0-0.25, self.cell_num-0.75)
            plt.yticks([])
            plt.title("Cell transmission model animation")
            plt.xlabel("Cell idx")
            
            curr = self.record[i]
            x, y = [idx for idx in range(self.cell_num)], [0 for idx in range(self.cell_num)]
            area = [2*num**2 for num in curr]       
            plt.scatter(x, y, color="red", s = area)
        if type==0:
            animation = FuncAnimation(fig, animation_func_0, frames=np.arange(0, len(self.record)))
        elif type==1:
            animation = FuncAnimation(fig, animation_func_1, frames=np.arange(0, len(self.record)))
        writergif = PillowWriter(15) 
        animation.save("anim_{}sec_{}.gif".format(self.dt*3600, type), writer=writergif)
        print("plot has been saved as anim_{}sec_{}.gif".format(self.dt*3600, type) )
        return

