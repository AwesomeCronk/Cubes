# File structure is as follows:
# imports
# exceptions
# shape classes
# main shader

#---------- imports ----------#
from OpenGL.GL import (
                       glLoadIdentity, glTranslatef, glRotatef,
                       glClear, glBegin, glEnd,
                       glColor3fv, glVertex3fv,
                       GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
                       GL_QUADS, GL_LINES
                      )
from OpenGL.GLU import gluPerspective

#---------- exceptions ----------#
class shapeNotFound(Exception):
    pass

#---------- shape classes ----------#
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

#---------- main shader ----------#
class shader():
    #variables
    parent = None
    shapes = []
    shapeTypes = [type(cube), type(mesh)]
    
    #functions
    def __init__(self, parent = None):
        self.parent = parent
        print('Initiated new shader as child of {}.'.format(self.parent))
    
    def resize(self, newSize):
        self.sizeX, self.sizeY = newSize
        
    def addShape(self, shapeIn):
        if type(shapeIn) not in self.shapeTypes:
            raise shapeNotFound("Shape {} not found.".format(shapeIn))
        self.shapes.append(shapeIn)
    
    def paintGL(self):
        #This function uses shape objects, such as cube() or mesh(). Shape objects require the following:
        #a list named 'vertices' - This list is a list of points, from which edges and faces are drawn.
        #a list named 'wires'    - This list is a list of tuples which refer to vertices, dictating where to draw wires.
        #a list named 'facets'   - This list is a list of tuples which refer to vertices, ditating where to draw facets.
        #a bool named 'render'   - This bool is used to dictate whether or not to draw the shape.
        #a bool named 'drawWires' - This bool is used to dictate whether wires should be drawn.
        #a bool named 'drawFaces' - This bool is used to dictate whether facets should be drawn.
        
        glLoadIdentity()
        gluPerspective(45, self.sizeX / self.sizeY, 0.1, 110.0)    #set perspective?
        glTranslatef(0, 0, self.zoomLevel)    #I used -10 instead of -2 in the PyGame version.
        glRotatef(self.rotateDegreeV, 1, 0, 0)    #I used 2 instead of 1 in the PyGame version.
        glRotatef(self.rotateDegreeH, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        if len(self.shapes) != 0:
            glBegin(GL_LINES)
            for s in self.shapes:
                glColor3fv(s.color)
                if s.render and s.drawWires:
                    for w in s.wires:
                        for v in w:
                            glVertex3fv(s.vertices[v])
            glEnd()
        
            glBegin(GL_QUADS)
            for s in self.shapes:
                glColor3fv(s.color)
                if s.render and s.drawFaces:
                    for f in s.facets:
                        for v in f:
                            glVertex3fv(s.vertices[v])
            glEnd()
