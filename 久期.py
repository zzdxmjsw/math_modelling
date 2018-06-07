import math

y = 0.07

def value():
    v = 0
    for i in range(1,9):
        v += 8 * math.e**(-y*i)
    v += 100 * math.e**(-8*y)
    return v

def duration():
    d = 0
    for i in range(1,9):
        d += 8 * i * math.e**(-y*i)

    d += 100 * math.e**(-8*y) * 8
    d /= value()
    return d

def convex():
    c = 0
    for i in range(1,9):
        c += 0.5 * 8 * (i)**2 * math.e**(-y*i)

    c += 0.5 * 100 * math.e**(-8*y) * 8**2
    c/= value()
    return c