import sys
from PyQt5.QtWidgets import (
                             QApplication, QMainWindow, QSlider,
                             QOpenGLWidget, QLabel, QPushButton
                            )
from PyQt5.QtCore import Qt
from OpenGL.GL import (
                       glLoadIdentity, glTranslatef, glRotatef,
                       glClear, glBegin, glEnd,
                       glColor3fv, glVertex3fv,
                       GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
                       GL_QUADS, GL_LINES
                      )
from OpenGL.GLU import gluPerspective
from numerics import sin, cos, tan, avg, rnd
from classes import *
from lookup import table
import random, time

class mainWindow(QMainWindow):    #Main class.
    shapes = []    #place all instaces of shapes in this list in order to have them rendered.
    dataPoints = []
    zoomLevel = -10
    rotateDegreeV = -90
    rotateDegreeH = 0
    marchActive = False
    limit = -1
    meshPoints = []
    meshSectors = []
    
    def keyPressEvent(self, event):    #This is the keypress detector.
        try:
            key = event.key()
        except:
            key = -1    
        #print(key)
        if key == 87:
            self.rotateV(5)
        elif key == 65:
            self.rotateH(5)
        elif key == 83:
            self.rotateV(-5)
        elif key == 68:
            self.rotateH(-5)
        elif key == 67:
            self.zoom(1)
        elif key == 88:
            self.zoom(-1)
        elif key == 77:
            self.marchStep()
            
    def __init__(self):
        super(mainWindow, self).__init__()
        self.currentStep = 0
        self.width = 700    #Variables used for the setting of the size of everything
        self.height = 600
        self.setGeometry(0, 0, self.width + 50, self.height)    #Set the window size
        self.initData(4, 4, 4)

    def setupUI(self):
        self.openGLWidget = QOpenGLWidget(self)    #Create the GLWidget
        self.openGLWidget.setGeometry(0, 0, self.width, self.height)
        self.openGLWidget.initializeGL()
        self.openGLWidget.resizeGL(self.width, self.height)    #Resize GL's knowledge of the window to match the physical size?
        self.openGLWidget.paintGL = self.paintGL    #override the default function with my own?

        self.filterSlider = QSlider(Qt.Vertical, self)
        self.filterSlider.setGeometry(self.width + 10, int(self.height / 2) - 100, 30, 200)
        self.filterSlider.valueChanged[int].connect(self.filter)
        
        self.limitDisplay = QLabel(self)
        self.limitDisplay.setGeometry(self.width, int(self.height / 2) - 130, 50, 30)
        self.limitDisplay.setAlignment(Qt.AlignCenter)
        self.limitDisplay.setText('-1')

        self.marchButton = QPushButton(self)
        self.marchButton.setGeometry(self.width, int(self.height / 2) - 160, 50, 30)
        self.marchButton.setText('March!')
        self.marchButton.clicked.connect(self.marchStep)

    def initData(self, sizeX, sizeY, sizeZ):
        marchSizeX = sizeX - 1
        marchSizeY = sizeY - 1
        marchSizeZ = sizeZ - 1
        xOff = -(sizeX / 2) + 0.5
        yOff = -(sizeY / 2) + 0.5
        zOff = -(sizeZ / 2) + 0.5
        xMarchOff = -(marchSizeX / 2) + 0.5
        yMarchOff = -(marchSizeY / 2) + 0.5
        zMarchOff = -(marchSizeZ / 2) + 0.5
        self.marchPoints = []
        for z in range(marchSizeZ):
            for y in range(marchSizeY):
                for x in range(marchSizeX):
                    self.marchPoints.append((x + xMarchOff, y + yMarchOff ,z + zMarchOff))

        for z in range(sizeZ):
            for y in range(sizeY):
                for x in range(sizeX):
                    val = self.generate(x + xOff, y + yOff, z + zOff)
                    dpColor = (0, (val + 1) / 2, (val + 1) / -2 + 1)
                    dpShape = cube((x + xOff, y + yOff, z + zOff), drawWires = False, drawFaces = True, color = dpColor)
                    dp = dataPoint((x + xOff, y + yOff, z + zOff), val, dpShape)
                    self.dataPoints.append(dp)
                    self.shapes.append(dpShape)

    def paintGL(self):
        #This function uses shape objects, such as cube() or meshSector(). Shape objects require the following:
        #a list named 'vertices' - This list is a list of points, from which edges and faces are drawn.
        #a list named 'wires'    - This list is a list of tuples which refer to vertices, dictating where to draw wires.
        #a list named 'facets'   - This list is a list of tuples which refer to vertices, ditating where to draw facets.
        #a bool named 'render'   - This bool is used to dictate whether or not to draw the shape.
        #a bool named 'drawWires' - This bool is used to dictate whether wires should be drawn.
        #a bool named 'drawFaces' - This bool is used to dictate whether facets should be drawn.
        
        glLoadIdentity()
        gluPerspective(45, self.width / self.height, 0.1, 110.0)    #set perspective?
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

    def marchStep(self):
        print(self.currentStep)
        if not self.marchActive:    #initialize
            marchAddr = len(self.shapes)
            self.marchingCube = cube(size = 1)
            self.shapes.append(self.marchingCube)
            self.marchActive = True
            self.currentStep = 0

        if self.currentStep == len(self.marchPoints):    #1 step after last
            self.marchingCube.hide()
            self.currentStep += 1
            for mp in self.meshPoints:
                mp.shape.hide()
            self.meshPoints = []
            self.openGLWidget.update()
            return
        if self.currentStep == len(self.marchPoints) + 1:    #2 steps after last
            #print('meshPoints: {}'.format(self.meshPoints))
            for mp in self.meshPoints:
                #print(mp.shape)
                self.shapes.remove(mp.shape)
            self.meshPoints.clear()
            for shape in self.shapes:
                if shape in self.meshSectors:
                    self.shapes.remove(shape)
            self.meshSectors = []
            self.currentStep = -1
            self.openGLWidget.update()
            return
            
        if self.currentStep == -1:    #1 step before first
            self.marchingCube.hide()
            self.currentStep += 1
            print('self.meshPoints: {}\nself.meshSectors: {}\nself.shapes: {}'.format(self.meshPoints, self.meshSectors, self.shapes))
            self.openGLWidget.update()
            return
            
        self.marchingCube.show()
        p = self.marchPoints[self.currentStep]
        x, y, z = p
        self.marchingCube.move((x, y, z))
        points = []
        for i in range(8):
            #print(self.marchingCube.vertices[i])
            point = self.getDataPointByLocation(self.marchingCube.vertices[i])
            points.append(point)
        
        #place meshpoints and highlight the active ones.
        MPs = []
        for pair in self.marchingCube.wires:
            pointA = points[pair[0]]
            pointB = points[pair[1]]
            #print('pointA.value: {}  pointB.value: {}  limit: {}'.formatpointA.value, pointB.value, self.limit)
            xA, yA, zA = pointA.location
            xB, yB, zB = pointB.location
            valA = (pointA.value + 1) / 2
            valB = (pointB.value + 1) / 2
            xC = float(avg([xA, xB]))
            yC = float(avg([yA, yB]))
            zC = float(avg([zA, zB]))
                
            mp = meshPoint()
            mp.place(xC, yC, zC)
            mp.setShape(cube(size = 0.05, drawWires = False, drawFaces = True, color = (1, 0, 0)))
            mp.shape.move((xC, yC, zC))
            self.shapes.append(mp.shape)
            self.meshPoints.append(mp)
            MPs.append(mp)
            if (pointA.value < self.limit and pointB.value > self.limit) or (pointA.value > self.limit and pointB.value < self.limit):
                mp.setActive(True)
            else:
                mp.setActive(False)
                
        activeConfig = 0
        sector = meshSector()
        self.meshSectors.append(sector)
        self.shapes.append(sector)
        
        for i in range(8):
            if points[i].value > self.limit:
                activeConfig += int(2 ** i)
        print('Configuration number: {}'.format(activeConfig))
        if activeConfig > 127:
            activeConfig = 255 - activeConfig
        print('Configuration number: {}'.format(activeConfig))
        
        config = table[activeConfig]
        print('Configuration: {}'.format(config))
        print('number of points: {}'.format(len(MPs)))
        for data in config:
            a, b, c = data
            locA = MPs[a].location
            locB = MPs[b].location
            locC = MPs[c].location
            sector.addFacet((locA, locB, locC))

        print('stepping')
        self.currentStep += 1
        self.rotateH(0)

    def zoom(self, value):
        self.zoomLevel += value
        self.openGLWidget.update()

    def rotateV(self, value):
        self.rotateDegreeV += value
        self.openGLWidget.update()

    def rotateH(self, value):
        self.rotateDegreeH += value
        self.openGLWidget.update()
        
    def filter(self, value):
        self.limit = rnd((value / 49.5) -1, -2)
        for d in self.dataPoints:
            if d.value < self.limit:
                d.shape.hide()
            else:
                d.shape.show()
        self.limitDisplay.setText(str(self.limit))
        self.openGLWidget.update()

    def getDataPointByLocation(self, coord):
        x, y, z = coord
        #print(self.dataPoints)
        #print('requested coordinates: {}'.format(coord))
        for dp in self.dataPoints:
            #print('dataPoint.location: {}'.format(dp.location))
            if dp.location == (x, y, z):
                return dp
        return False

    def generate2(self, xIn, yIn, zIn):
        if xIn == 0 and yIn == 0 and zIn == 0:
            return 0.5
        return -0.5
        
    def generate(self, xIn, yIn, zIn):    #Function which produces semi-random values based on the supplied coordinates.
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
        return float(out / 10)

    #classes------------------------------------------------------------
    

app = QApplication([])
window = mainWindow()
window.setupUI()
window.show()
sys.exit(app.exec_())