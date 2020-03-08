class cube():
    render = True
    def __init__(self, location = (0, 0, 0), size = 0.1, drawWires = True, drawFaces = False, color = (1, 1, 1)):
        self.location = location
        self.size = size
        self.drawWires = drawWires
        self.drawFaces = drawFaces
        self.color = color
        self.compute()

    def compute(self):
        x, y, z = self.location
        s = self.size / 2
        self.vertices = [    #8 corner points calculated in reference to the supplied center point
                         (-s + x, s + y, -s + z), (s + x, s + y, -s + z),
                         (s + x, -s + y, -s + z), (-s + x, -s + y, -s + z),
                         (-s + x, s + y, s + z), (s + x, s + y, s + z),
                         (s + x, -s + y, s + z), (-s + x, -s + y, s + z)
                        ]
        self.wires = [    #12 tuples referencing the corner points
                      (0,1), (0,3), (0,4), (2,1), (2,3), (2,6),
                      (7,3), (7,4), (7,6), (5,1), (5,4), (5,6)
                     ]
        self.facets = [    #6 tuples referencing the corner points
                       (0, 1, 2, 3), (0, 1, 6, 5), (0, 3, 7, 4),
                       (6, 5, 1, 2), (6, 7, 4, 5), (6, 7, 3, 2)
                      ]
    def show(self):
        self.render = True
    def hide(self):
        self.render = False
    def move(self, location):
        self.location = location
        self.compute()
    def recolor(self, col):
        if type(col) is tuple:
            self.color = col
    
class dataPoint():
    def __init__(self, location = (0, 0, 0), value = 0, shape = None):
        self.location = location
        self.value = value
        self.shape = shape
    def place(self, x, y, z):
        self.location = (x, y, z)
    def set(self, val):
        self.value = val
    def setShape(self, shape):
        self.shape = shape
            
class meshPoint():
    active = False
    def __init__(self, location = (0, 0, 0), shape = None):
        self.location = location
        self.shape = shape
        if self.shape != None:
            #print('{} is hiding shape'.format(self))
            self.shape.hide()
    def place(self, x, y, z):
        self.location = (x, y, z)
    def setShape(self, shape):
        self.shape = shape
        if self.shape != None:
            #print('{} is hiding shape'.format(self))
            self.shape.hide()
    def setActive(self, state):
        self.active = state
        if self.active and self.shape != None:
            #print('{} is showing shape'.format(self))
            self.shape.show()
        elif self.shape != None:
            #print('{} is hiding shape'.format(self))
            self.shape.hide()

class mesh():
    vertices = []
    facets = []
    wires = []
    render = True
    def __init__(self, drawWires = True, drawFaces = False, color = (1, 1, 1)):
        self.drawWires = drawWires
        self.drawFaces = drawFaces
        self.color = color
        self.vertices = []
        self.facets = []
        self.wires = []
        self.render = True
    def addFacet(self, coords):    #takes a tuple of three location tuples.
        addr = len(self.vertices)
        addrs = [None, None, None]
        for i in range(3):
            c = coords[i]
            if not c in self.vertices:
                self.vertices.append(c)
            addrs[i] = self.vertices.index(c)

        self.facets.append((addrs[0], addrs[1], addrs[2]))
        self.wires.append((addrs[0], addrs[1]))
        self.wires.append((addrs[2], addrs[1]))
        self.wires.append((addrs[2], addrs[0]))

