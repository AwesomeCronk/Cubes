import sys
from PyQt5.QtWidgets import (
                             QApplication, QMainWindow, QSlider,
                             QOpenGLWidget, QLabel, QPushButton
                            )
from PyQt5.QtCore import Qt, QTimer
from numerics import sin, cos, tan, avg, rnd
from classes import *
from lookup import table
from utilities import generate
from shaderProgram import shader, cube, mesh
import time

class mainWindow(QMainWindow):    #Main class.
    shapes = []    #place all instances of shapes in this list in order to have them rendered.
    dataPoints = []
    zoomLevel = -10
    rotateDegreeV = -90
    rotateDegreeH = 0
    marchActive = False
    limit = -1
    meshPoints = []
    dataFieldSize = (3, 3, 3)
    
    def keyPressEvent(self, event):    #This is the keypress detector.
        try:
            key = event.key()
        except:
            key = -1    
        #print(key)
        if key == 87:
            self.nav(vVal = 5)
        elif key == 65:
            self.nav(hVal = 5)
        elif key == 83:
            self.nav(vVal = -5)
        elif key == 68:
            self.nav(hVal = -5)
        elif key == 67:
            self.nav(zVal = 1)
        elif key == 88:
            self.nav(zVal = -1)
        elif key == 77:
            self.marchStep()
        elif key == 16777216:
            exit()
            
    def __init__(self):
        super(mainWindow, self).__init__()
        self.shader = shader(self)
        self.currentStep = 0
        self.sizeX = 700    #Variables used for the setting of the size of everything
        self.sizeY = 600
        self.shader.resize((self.sizeX, self.sizeY))
        self.setGeometry(0, 0, self.sizeX + 50, self.sizeY)    #Set the window size
        self.initData(self.dataFieldSize)
        self.setupUI()

    def setupUI(self):
        self.openGLWidget = QOpenGLWidget(self)    #Create the GLWidget
        self.openGLWidget.setGeometry(0, 0, self.sizeX, self.sizeY)
        self.openGLWidget.initializeGL()
        self.openGLWidget.resizeGL(self.sizeX, self.sizeY)    #Resize GL's knowledge of the window to match the physical size?
        self.openGLWidget.paintGL = self.shader.paintGL    #override the default function with my own?

        self.filterSlider = QSlider(Qt.Vertical, self)
        self.filterSlider.setGeometry(self.sizeX + 10, int(self.sizeY / 2) - 100, 30, 200)
        self.filterSlider.valueChanged[int].connect(self.filter)
        
        self.limitDisplay = QLabel(self)
        self.limitDisplay.setGeometry(self.sizeX, int(self.sizeY / 2) - 130, 50, 30)
        self.limitDisplay.setAlignment(Qt.AlignCenter)
        self.limitDisplay.setText('-1')

        self.marchButton = QPushButton(self)
        self.marchButton.setGeometry(self.sizeX, int(self.sizeY / 2) - 160, 50, 30)
        self.marchButton.setText('March!')
        self.marchButton.clicked.connect(self.marchStep)

    def initData(self, size):
        sizeX, sizeY, sizeZ = size
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
                    val = generate(x + xOff, y + yOff, z + zOff)
                    dpColor = (0, (val + 1) / 2, (val + 1) / -2 + 1)
                    dpShape = cube((x + xOff, y + yOff, z + zOff), drawWires = False, drawFaces = True, color = dpColor)
                    dp = dataPoint((x + xOff, y + yOff, z + zOff), val, dpShape)
                    self.dataPoints.append(dp)
                    self.shapes.append(dpShape)

    def marchStep(self):
        #print(self.currentStep)
        if not self.marchActive:    #initialize
            marchAddr = len(self.shapes)
            self.marchingCube = cube(size = 1)
            self.shapes.append(self.marchingCube)
            self.marchActive = True
            self.currentStep = 0
            self.mainMesh = mesh()
            self.shapes.append(self.mainMesh)
            self.marchTimer = QTimer()
            self.marchTimer.start(250)
            self.marchTimer.timeout.connect(self.marchStep)

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
            self.shapes.remove(self.mainMesh)
            self.meshes = []
            self.currentStep = -1
            self.openGLWidget.update()
            return
            
        if self.currentStep == -1:    #1 step before first
            self.marchingCube.hide()
            self.currentStep += 1
            #print('self.meshPoints: {}\nself.meshes: {}\nself.shapes: {}'.format(self.meshPoints, self.meshes, self.shapes))
            self.openGLWidget.update()
            self.mainMesh = mesh()
            self.shapes.append(self.mainMesh)
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
        for i in range(8):
            if points[i].value > self.limit:
                activeConfig += int(2 ** i)
        #print('Configuration number: {}'.format(activeConfig))
        if activeConfig > 127:
            activeConfig = 255 - activeConfig
        #print('Configuration number: {}'.format(activeConfig))
        
        config = table[activeConfig]
        #print('Configuration: {}'.format(config))
        #print('number of points: {}'.format(len(MPs)))
        for data in config:
            a, b, c = data
            locA = MPs[a].location
            locB = MPs[b].location
            locC = MPs[c].location
            self.mainMesh.addFacet((locA, locB, locC))

        #print('stepping')
        self.currentStep += 1
        self.openGLWidget.update()

    def nav(self, hVal = 0, vVal = 0, zVal = 0):
        self.shader.navigate(hVal, vVal, zVal)
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

app = QApplication([])
window = mainWindow()
window.show()
sys.exit(app.exec_())