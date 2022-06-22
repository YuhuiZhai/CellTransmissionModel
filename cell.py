class Cell:
    def __init__(self, id, length, n, Q, N, weight=0):
        self.id, self.length, self.n, self.Q, self.N, self.weight = id, length, n, Q, N, weight
        self.blocked = False
        self.next_cell = None
        self.y_in, self.y_out = 0, 0
        self.position = ()
        self.status, self.merged_cell = 0, None
        
    def linkNext(self, next_cell):
        self.next_cell = next_cell
        return 

    def transferNext(self):
        if self.next_cell == None or self.blocked: return 0
        elif self.status == 0: 
            y = min(self.n, self.Q, self.next_cell.N-self.next_cell.n)
            self.y_out += y
            self.next_cell.y_in += y
        elif self.status == 1: 
            y = self.mergeflow()
            self.y_out += y
            self.next_cell.y_in += y
        elif self.status == 2:
            y = self.divergeflow()
            self.y_out += y
            for c in self.next_cell:
                c.y_in += y        
        return y 
    
    def update(self):
        if self.id == 'g': return self.n
        elif self.id == 'e': self.n = self.y_in
        else: self.n = self.n - self.y_out + self.y_in
        self.y_in, self.y_out = 0, 0
        return self.n
    
    def getMid(self, a, b, c):
        if a > b :
            if (b > c): return b
            elif (a > c): return c
            else: return a
        else:
            if (a > c): return a
            elif (b > c): return c
            else: return b

    # function to derive flow of merge scenario
    def mergeflow(self):
        Ck = self.merged_cell
        Ek = self.next_cell
        Sbk, Sck = min(self.Q, self.n), min(Ck.Q, Ck.n)
        Rek = min(Ek.Q, Ek.N-Ek.n)
        pbk = self.weight/(self.weight+Ck.weight)
        if Rek < (Sbk + Sck): ybk = self.getMid(Sbk, Rek-Sck, pbk*Rek) 
        else: ybk = Sbk
        return ybk

    def divergeflow(self):
        Sbk = min(self.Q, self.n)
        weights = sum([c.weight for c in self.next_cell])
        ybk = min(Sbk, *[min(c.Q, c.N-c.n)/(c.weight/weights) for c in self.next_cell])
        return ybk

