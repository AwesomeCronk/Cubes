import random
from numerics import sin, cos, tan, avg, rnd, abs

def locByVal(val):
    return (
            (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5, -0.5, -0.5),
            (-0.5, -0.5, -0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5),
            (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5)
           )[val]
        
def generate2(x, y, z):
    a = ((x ** 2) + y) * float(tan(x)) * y * float(cos(z))
    if a != 0:
        return -1 * float(abs(1 / a))
    else:
        return 0

def generate(xIn, yIn, zIn):    #Function which produces semi-random values based on the supplied coordinates.
    i = -int(xIn * yIn * (10 + zIn))
    j = int(xIn * yIn * (10 + zIn))
    if i < j:
        mixer = random.randint(i, j + 1)
    else:
        mixer = random.randint(j, i + 1)
    a = avg([sin(cos(xIn)), tan(tan(yIn)), cos(tan(zIn))])
    out = mixer * a
    while out > 10:
        out -= 5
    while out < -10:
        out += 5
    return float(-out / 10)
    
def center(self, xIn, yIn, zIn):
    if xIn == 0 and yIn == 0 and zIn == 0:
        return 0.5
    return -0.5

def intToBin(intIn):
    rawBin = bin(intIn)
    length = len(rawBin) - 2
    newBin = []
    for i in range(length):
        newBin.append(int(rawBin[i + 2]))
    while len(newBin) < 8:
        newBin.insert(0, 0)
    return newBin
    
def getDPByCoord(list, coord):
    x, y, z = coord
    #print(self.dataPoints)
    #print('requested coordinates: {}'.format(coord))
    for dp in list:
        #print('dataPoint.location: {}'.format(dp.location))
        if dp.location == (x, y, z):
            return dp
    return False
    
