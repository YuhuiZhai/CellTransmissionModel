def getMid(a, b, c):
    if a > b :
        if (b > c): return b
        elif (a > c): return c
        else: return a
    else:
        if (a > c): return a
        elif (b > c): return c
        else: return b

print(getMid(2.0,2.5,3.0))