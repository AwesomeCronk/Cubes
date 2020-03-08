import sys, random, time
from PyQt5.QtWidgets import (
                             QApplication, QMainWindow, QSlider,
                             QOpenGLWidget, QLabel, QPushButton,
                             QWidget
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
from utilities import locByVal, intToBin

class mainWindow(QMainWindow):    #Main class.
    shapes = []    #place all instaces of shapes in this list in order to have them rendered.
    dataPoints = []
    zoomLevel = -5
    rotateDegreeV = -90
    rotateDegreeH = 0
    marchActive = False
    limit = 0.5
    meshPoints = []
    step = 0
    pairs = [
             (0,1), (0,3), (0,4), (2,1), (2,3), (2,6),
             (7,3), (7,4), (7,6), (5,1), (5,4), (5,6)
            ]
    
    def __init__(self):
        super(mainWindow, self).__init__()
        self.currentStep = 0
        self.width = 700    #Variables used for the setting of the size of everything
        self.height = 600
        self.setGeometry(0, 0, self.width + 50, self.height + 25)    #Set the window size
        self.initData()
        self.shapes.append(cube((0, 0, 0)))
        self.shapes.append(cube((0, -1, 0)))
        for i in range(12):
            locA = locByVal(self.pairs[i][0])
            locB = locByVal(self.pairs[i][1])
            loc = (float(avg((locA[0], locB[0]))), float(avg((locA[1], locB[1]))), float(avg((locA[2], locB[2]))))
            shape = cube(loc, 0.05, False, True, (1, 0, 0))
            self.meshPoints.append(shape)
            self.shapes.append(shape)
            #print(loc)

    def setupUI(self):
        self.openGLWidget = QOpenGLWidget(self)    #Create the GLWidget
        self.openGLWidget.setGeometry(0, 0, self.width, self.height)
        self.openGLWidget.initializeGL()
        self.openGLWidget.resizeGL(self.width, self.height)    #Resize GL's knowledge of the window to match the physical size?
        self.openGLWidget.paintGL = self.paintGL    #override the default function with my own?

        self.marchButton = QPushButton(self)
        self.marchButton.setGeometry(350, self.height, 60, 25)
        self.marchButton.setText('Step 0')
        self.marchButton.clicked.connect(self.cycle)
        
        self.readout = QLabel(self)
        self.readout.setGeometry(240, self.height, 110, 25)
        self.readout.setText("[0, 0, 0, 0, 0, 0, 0, 0]")
        
        self.indicators = []
        for i in range(8):
            indicator = QWidget(self)
            indicator.setGeometry(i * 30, self.height, 25, 25)
            indicator.setStyleSheet("background-color: blue;")
            self.indicators.append(indicator)

    def initData(self):
        for i in range(8):
            loc = locByVal(i)
            col = (0, 0.5, 0.5)
            shape = cube(location = loc, drawWires = False, drawFaces = True, color = col)
            dp = dataPoint(location = loc, value = 0.5, shape = shape)
            self.dataPoints.append(dp)
            self.shapes.append(dp.shape)

    def paintGL(self):
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
    
    def keyPressEvent(self, event):    #This is the keypress detector. I use this to determine input to edit grids.
        try:
            key = event.key()
            #print(key)
            if key == 87:
                self.nav(rotV = 5)
            elif key == 65:
                self.nav(rotH = 5)
            elif key == 83:
                self.nav(rotV = -5)
            elif key == 68:
                self.nav(rotH = -5)
            elif key == 67:
                self.nav(zoomVal = 1)
            elif key == 88:
                self.nav(zoomVal = -1)
            elif key == 82:
                self.cycle('up')
            elif key == 70:
                self.cycle('down')
        except:
            pass

    def nav(self, zoomVal = 0, rotV = 0, rotH = 0):
        self.zoomLevel += zoomVal
        self.rotateDegreeV += rotV
        self.rotateDegreeH += rotH
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

    def getDP(self, coord):
        x, y, z = coord
        #print(self.dataPoints)
        #print('requested coordinates: {}'.format(coord))
        for dp in self.dataPoints:
            #print('dataPoint.location: {}'.format(dp.location))
            if dp.location == (x, y, z):
                return dp
        return False
        
    def cycle(self, dir = 'up'):
        #housekeeping
        if dir == 'up':
            if self.step == 255:
                self.step = 0
            else:
                self.step += 1
        elif dir == 'down':
            if self.step == 0:
                self.step = 255
            else:
                self.step -= 1

        #set the points
        self.marchButton.setText("Step " + str(self.step))
        binDat = intToBin(self.step)
        self.readout.setText(str(binDat))
        for dp in self.dataPoints:
            dp.shape.recolor((0, 0.5, 0.5))
        for indi in self.indicators:
            indi.setStyleSheet("background-color: blue;")
        for i in range(8):
            rawDat = binDat[7 - i]
            dat = (rawDat - 0.5) * 2    #0 --> -1  1 --> 1
            self.dataPoints[i].set(dat)
            self.dataPoints[i].shape.recolor((0, rawDat, 1 - rawDat))
            if dat == 1:
                self.indicators[7 - i].setStyleSheet("background-color: green;")
        
        #show/hide the meshPoints
        for i in range(12):
            pointA = self.dataPoints[self.pairs[i][0]]
            pointB = self.dataPoints[self.pairs[i][1]]
            if pointA.value != pointB.value:
                self.meshPoints[i].show()
            else:
                self.meshPoints[i].hide()
        
        self.openGLWidget.update()

app = QApplication([])
window = mainWindow()
window.setupUI()
window.show()
sys.exit(app.exec_())