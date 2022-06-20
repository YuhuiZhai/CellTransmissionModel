import heapq as hq
def getMid(a, b, c):
    d = []
    hq.heappush(d, (a, a))
    hq.heappush(d, (b, b))
    hq.heappush(d, (c, c))
    mid = d[1][0]
    return mid

# function to derive flow of merge scenario
def merge(Bk, Ck, Ek):
    Sbk, Sck = min(Bk.Q, Bk.n), min(Ck.Q, Ck.n)
    Rek = min(Ek.Q, Ek.N-Ek.n)
    pbk, pck = Bk.weight/(Bk.weight+Ck.weight), Ck.weight/(Bk.weight+Ck.weight)
    if Rek < (Sbk + Sck):
        ybk = getMid(Sbk, Rek-Sck, pbk*Rek)
        yck = getMid(Sck, Rek-Sbk, pck*Rek)
    else:
        ybk = Sbk
        yck = Sck
    return (ybk, yck)


