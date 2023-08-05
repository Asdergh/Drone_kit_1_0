import pyqtgraph as pg
from pyqtgraph import opengl as gl
from pyqtgraph import QtCore, QtGui, QtWidgets
import numpy as np
import sys



class Vizualizer():

    def __init__(self) -> None:
        
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = gl.GLViewWidget()
        self.window.setGeometry(0, 110, 1200, 1800)
        self.window.show()
        self.window.setWindowTitle("Scatter test")
        self.window.setCameraPosition(distance=30, elevation=8)

        self.x = np.linspace(-np.pi, np.pi, 100)
        self.y = np.linspace(-np.pi, np.pi, 100)
        self.x_grid, self.y_grid = np.meshgrid(self.x, self.y)
        self.z = np.sin(np.sqrt(self.x_grid ** 2 + self.y_grid ** 2)) / np.sqrt(self.x_grid ** 2 + self.y_grid ** 2)
        self.colors = np.array([np.random.randint(5, 100), np.random.randint(5, 100),
                                 np.random.randint(5, 100)])
        self.iter = 0

    def first_object_creation(self):

        self.volume = gl.GLSurfacePlotItem(self.x, self.y, self.z, colors=self.colors)
        self.grid = gl.GLGridItem()
        self.grid.scale(2, 2, 2)
        self.window.addItem(self.volume)
        self.window.addItem(self.grid)
    
    def changing_object_propertys(self):

        self.x = np.linspace(-np.pi, np.pi, 100)
        self.y = np.linspace(-np.pi, np.pi, 100)
        self.x_grid, self.y_grid = np.meshgrid(self.x, self.y)
        self.z = np.sin(np.sqrt(self.x_grid ** 2 + self.iter + self.y_grid ** 2 * 2 + self.iter)) / np.sqrt(self.x_grid ** 2 + self.iter + self.y_grid ** 2 + self.iter)

        self.colos = self.colors = np.array([np.random.normal(100, 256), np.random.normal(100, 256),
                                 np.random.normal(100, 256)])
        
        self.volume.setData(self.x, self.y, self.z, colors=self.colors)
        self.iter = self.iter + 0.989898989 * np.random.normal(0.1, 0.1)
        print(f"[color cores x: {self.colors[0]}, colors core y: {self.colors[1]}, color cores z: {self.colors[2]}] ========= general list of color cores: {self.colors}")
    
    def demo_animation(self):

        self.time = QtCore.QTimer()
        self.time.timeout.connect(self.changing_object_propertys)
        self.time.start(10)
        self.start()
        self.changing_object_propertys()


    def start(self):

        self.first_object_creation()
        if (sys.flags.interactive != 1) or not hasattr(QtCore, "PYQT_VERSION"):
            QtGui.QGuiApplication.instance().exec_()


obj = Vizualizer()
obj.demo_animation()


        
    