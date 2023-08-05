from typing import Any
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np




class Dinemic_drone_tools():

    # инициализируем класс динамических рассчетов
    def __init__(self, B, velocity, position,
                  acceleration, rotor_count, copter_mass, dt) -> None:
        
        self.B = B
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.rotor_count = rotor_count
        self.rotor_acceleration_sum = 0
        self.copter_mass = copter_mass
        self.g = 9.8
        self.dt = dt
    
    #рассчитываем ускорение системы
    def calculate_acceleration(self, rotor_acceleration):
        
        for _ in range(self.rotor_count):
            self.rotor_acceleration_sum += rotor_acceleration ** 2
        
        self.acceleration = (self.rotor_acceleration_sum * self.B) / self.copter_mass - self.g

    #рассчитываем скорость и положение системы
    def calculate_vel_and_pos(self, integr_dt):

        self.velocity += self.velocity * integr_dt
        self.position += self.position * integr_dt

    #инициализируем необхадимые рассчеты
    def general_calculations(self, U, dt):

        self.calculate_acceleration(rotor_acceleration=U)
        self.calculate_vel_and_pos(integr_dt=self.dt)

class Contrall_sistem(Dinemic_drone_tools):

    def __init__(self, B, velocity, position, acceleration,
                  rotor_count, copter_mass, K_d, K_i, K_p, sat_limit, dt) -> None:
        
        super().__init__(B, velocity, position, acceleration, rotor_count, copter_mass, dt)
        self.saturation_limit = sat_limit
        self.disired_sistem_position = 0
        self.K_d = K_d
        self.K_p = K_p
        self.K_i = K_i
        self.error_previous = 0
        self.pid_integral = 0
    
    def set_disired_position(self, ds_pos):
        self.disired_sistem_position = ds_pos

    def calculate_U_PID(self, dt, curent_sistem_position):

        self.error = self.disired_sistem_position - curent_sistem_position

        self.pid_integral += self.error * dt
        self.U = self.K_p * self.error + self.K_i * self.pid_integral + self.K_d * ((self.error - self.error_previous) / dt)
        
        self.error_previous = self.error
        self.sistem_saturation()

    
    def sistem_saturation(self):

        if self.U > self.saturation_limit:
            self.U = self.saturation_limit
        
        elif self.U < -self.saturation_limit:
            self.U = self.saturation_limit

class Sistem_Sumulation(Contrall_sistem):

    def __init__(self, B, velocity, position, acceleration, rotor_count, copter_mass, K_d, K_i, K_p, sat_limit, dt, simulation_episodes) -> None:

        super().__init__(B, velocity, position, acceleration, rotor_count, copter_mass, K_d, K_i, K_p, sat_limit, dt)
        self.simulation_episodes = simulation_episodes
        self.figure = plt.figure()
        self.axis_1 = self.figure.add_subplot()
        self.axis_2 = self.figure.add_subplot()
        self.axis_3 = self.figure.add_subplot()

        self.sistem_position_list = []
        self.sistem_velocity_list = []
        self.sistem_acceleration_list = []

    

    def run_simulation(self):

        def animation(time):
            self.axis_1.clear()
            self.axis_2.clear()
            self.axis_2.clear()

            self.calculate_U_PID(dt=self.dt, curent_sistem_position=self.position)
            self.general_calculations(U=self.U, dt=self.dt)
            
            self.sistem_position_list.append(self.position)
            self.sistem_velocity_list.append(self.velocity)
            self.sistem_acceleration_list.append(self.acceleration)

            self.axis_1.plot(self.sistem_position_list, label="position info", color="blue")
            self.axis_2.plot(self.sistem_velocity_list, label="velocity info", color="red")
            self.axis_3.plot(self.sistem_acceleration_list, label="acceleration info", color="green")

        self.demo = FuncAnimation(self.figure, animation, interval=self.simulation_episodes)
        self.axis_1.legend(loc="upper left")
        self.axis_2.legend(loc="upper left")
        self.axis_3.legend(loc="upper left")

        plt.show()




k_p = 150
k_i = 0
k_d = 30
dt = 0.01
T_end = 150
mass = 0.006
B = 3.9865e-08
motor_spid_limit = 1000

sim = Sistem_Sumulation(K_i=k_i, K_d=k_d, K_p=k_p, sat_limit=motor_spid_limit, simulation_episodes=T_end, copter_mass=mass, B=B, position=0, 
                        velocity=0, acceleration=0, rotor_count=4, dt=dt)
sim.set_disired_position(10)
sim.run_simulation()



            






    




        
        

        