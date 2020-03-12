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
            