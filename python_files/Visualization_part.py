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
        
        self.object_position_x_list = [2.9898]
        self.object_position_y_list = [2.9898]
        self.object_position_z_list = [2.9898]


        self.sigma = 0.7891
        self.zeta = 0.123
        self.beta = 12.567


        self.item_index = 0
        self.iter = 0

    def first_object_creation(self):

        self.surface = gl.GLSurfacePlotItem(self.x, self.y, self.z, colors=self.colors)
        self.grid = gl.GLGridItem()

        self.general_cores = np.array([np.asarray(self.object_position_x_list), np.asarray(self.object_position_y_list),
                                       np.asarray(self.object_position_z_list)])


        self.curve = gl.GLLinePlotItem(pos=self.general_cores, color=np.array([100, 100, 256]))
        self.grid.scale(2, 2, 2)
        self.window.addItem(self.surface)
        self.window.addItem(self.grid)
    
    def changing_object_propertys(self):

        self.x = np.linspace(-np.pi, np.pi, 100)
        self.y = np.linspace(-np.pi, np.pi, 100)
        self.x_grid, self.y_grid = np.meshgrid(self.x, self.y)
        self.z = np.sin(np.sqrt(self.x_grid ** 2 + self.iter + self.y_grid ** 2 * 2 + self.iter)) / np.sqrt(self.x_grid ** 2 + self.iter + self.y_grid ** 2 + self.iter)

        self.x_linear = self.object_position_x_list[self.item_index] - self.object_position_y_list[self.item_index]
        self.y_linear = self.object_position_x_list[self.item_index] * (self.zeta - self.object_position_z_list[self.item_index])
        self.z_linear = self.object_position_x_list[self.item_index] * self.object_position_y_list[self.item_index] - self.beta * self.object_position_z_list[self.item_index]

        self.object_position_x_list.append(self.x_linear)
        self.object_position_y_list.append(self.y_linear)
        self.object_position_z_list.append(self.z_linear)

        self.array_form_x_linear = np.asarray(self.object_position_x_list)
        self.array_form_y_linear = np.asarray(self.object_position_y_list)
        self.array_form_z_linear = np.asarray(self.object_position_z_list)

        self.curent_general_cores = np.array([np.asarray(self.array_form_x_linear), np.asarray(self.array_form_y_linear), 
                                              np.asarray(self.array_form_z_linear)]).T
        print(self.curent_general_cores)
        self.colos = np.array([np.random.normal(100, 256), np.random.normal(100, 256),
                                 np.random.normal(100, 256)])
        self.curve_colors = np.array([100, 100, 256])
        
        self.surface.setData(self.x, self.y, self.z, colors=self.colors)
        self.curve.setData(pos=self.curent_general_cores, color=self.curve_colors)
        
        self.iter = self.iter + 0.989898989 * np.random.normal(0.1, 0.1)
        print(f"[color cores x: {self.colors[0]}, colors core y: {self.colors[1]}, color cores z: {self.colors[2]}] ========= general list of color cores: {self.colors}")
        self.item_index += 1


    
    def demo_animation(self):

        self.time = QtCore.QTimer()
        self.time.timeout.connect(self.changing_object_propertys)
        self.time.start(100)
        self.start()
        self.changing_object_propertys()


    def start(self):

        self.first_object_creation()
        if (sys.flags.interactive != 1) or not hasattr(QtCore, "PYQT_VERSION"):
            QtGui.QGuiApplication.instance().exec_()


class Matplotlib_Visualiser():

    def __init__(self, rotor_coeef, rotor_mass, rotor_count=4, start_velocity=0, start_acceleration=0) -> None:
        
        self.sistem_object_velocity_list = []
        self.sistem_object_acceleration_list = []
        self.sistem_angular_velocity = []

        self.differential_of_time = 0.01

        self.rotor_count = rotor_count
        self.rotor_angular_velocity = 12.234
        self.rotor_angular_velocity_sum = 0
        self.rotor_coeef = rotor_coeef
        self.copter_mass = rotor_mass
        self.g_coeff = 9.81

        self.sistem_curent_velocity = start_velocity
        self.sistem_curent_acceleration = start_acceleration
        self.sistem_curent_position = 0
        

    
    def calculate_acceleration(self):

        for _ in range(self.rotor_count):
            self.rotor_angulat_velocity_sum += self.rotor_angular_velocity
        
        self.sistem_curent_acceleration = (self.rotor_angular_velocity_sum * self.rotor_coeef) / self.copter_mass - self.g_coeff
    
    def caculate_position_and_velocity(self):

        self.sistem_curent_velocity += self.sistem_curent_acceleration * self.differential_of_time
        self.sistem_curent_position += self.sistem_curent_position * self.differential_of_time
    
    def 



obj = Vizualizer()
obj.demo_animation()


        
    