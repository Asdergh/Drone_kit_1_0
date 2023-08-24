from typing import Any
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np



plt.style.use("seaborn")

# 
class Dinemic_drone_tools():

    # инициализируем класс динамических рассчетов
    def __init__(self, B, velocity, position,
                  acceleration, rotor_count, copter_mass, dt) -> None:
                  
        # !variable B: коэффициент тяги роторов
        # !type B: float

        # !varibale position: положение БЛА
        # !type position: float
        
        # !variable velocity: скорость БЛА
        # !type velocity: float
        
        # !variabel acceleration: ускорение БЛА
        # !type acceleration: float
        
        # !variabel rotor_count: колчичество роторов
        # !type rotor_count: int
        
        # !variable rotor_acceleration_sum: сумма угловых скоростей ротов
        # !type rotor_acceleration_sum: float
        
        # !variable copter_mass: масса БЛА
        # !type copter_mass: flaot
        
        # !variable g: коэффициент свободного падения
        # !type g: float
        
        # !variable dt: шаг дифференциирования и интегрирования
        # !type dt: float

        self.B = B
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.rotor_count = rotor_count
        self.rotor_acceleration_sum = 0
        self.copter_mass = copter_mass
        self.g = 9.81
        self.dt = dt
    
    #рассчитываем ускорение системы
    def calculate_acceleration(self, rotor_acceleration):
        
        for _ in range(self.rotor_count):
            self.rotor_acceleration_sum += rotor_acceleration ** 2
        
        self.acceleration = ((self.rotor_acceleration_sum * self.B) / self.copter_mass) - self.g

    #рассчитываем скорость и положение системы
    def calculate_vel_and_pos(self):

        self.velocity += self.acceleration * self.dt
        self.position += self.velocity * self.dt

    #инициализируем необхадимые рассчеты
    def general_calculations(self):

        self.calculate_acceleration(rotor_acceleration=self.U)
        self.calculate_vel_and_pos()


# класс для расчета системы управления ===========================================================================
class Contrall_sistem(Dinemic_drone_tools):

    # инициализируем класс
    def __init__(self, B, velocity, position, acceleration,
                  rotor_count, copter_mass, K_d, K_i, K_p, sat_limit, dt) -> None:
        
        # variable saturation_limit: ограничения максимальной и минимальной угловой скорости роторов
        # type saturation_limit: int

        # variable didired_sistem_position: желаемое положение системы
        # type: int

        # variable K_d: коээфициент диффиренциирования
        # type: float

        # variable K_p: коэффициент П регулятора
        # type: float

        # variable K_i: коэффициент интегрирования
        # type: float

        # variable error_previous: (i - 1) - я ошибка
        # type error_previous: flaot

        # variable pid_integral: интеграл для И регулятора
        # type pid_integral: flaot

        
        super().__init__(B, velocity, position, acceleration, rotor_count, copter_mass, dt)
        self.saturation_limit = sat_limit
        self.disired_sistem_position = 0.0
        self.K_d = K_d
        self.K_p = K_p
        self.K_i = K_i
        self.error_previous = 0
        self.pid_integral = 0
    
    #задаем желаемое положение системы
    def set_disired_position(self, ds_pos):
        self.disired_sistem_position = ds_pos

    # подсчитываем управляющее взаимодействие
    def calculate_U_PID(self, curent_sistem_position):

        self.error = self.disired_sistem_position - curent_sistem_position

        self.pid_integral += self.error * self.dt
        self.U = self.K_p * self.error + self.K_i * self.pid_integral + self.K_d * ((self.error - self.error_previous) / self.dt)
        
        self.error_previous = self.error
        self.sistem_saturation()

    # фильтруем управляющее взаимодействие
    def sistem_saturation(self):

        if self.U > self.saturation_limit:
            self.U = self.saturation_limit
        
        elif self.U < -self.saturation_limit:
            self.U = -self.saturation_limit

# класс симултор для реализации алгоритма ==========================================================================================
class Sistem_Sumulation(Contrall_sistem):

    # инициализируем класс
    def __init__(self, B, velocity, position, acceleration, rotor_count, copter_mass, K_d, K_i, K_p, sat_limit, dt, simulation_episodes) -> None:
        
        # variable simulation_episode: кол-во эпизодов системы
        # type: int

        # variable figure: обект для изображения графиков
        # type figure: plt_object

        # variable sistem_position_list: лист значений положения БЛА
        # type sistem_position_list: list

        # variable sistem_veclocity_list: лист для значений скорости БЛА
        # type sistem_velocity_list: list

        # variable sistem_acceleration_list: лист для значений ускоерения БЛА
        # type sistem_acceleration_list: list


        super().__init__(B, velocity, position, acceleration, rotor_count, copter_mass, K_d, K_i, K_p, sat_limit, dt)
        self.simulation_episodes = simulation_episodes
        self.figure = plt.figure(constrained_layout=True)
        self.grid = self.figure.add_gridspec(3, 5)

        self.axis_1 = self.figure.add_subplot(self.grid[0, :-1])
        self.axis_2 = self.figure.add_subplot(self.grid[1, :-1])
        self.axis_3 = self.figure.add_subplot(self.grid[2, :-1])

        self.sistem_position_list = []
        self.sistem_velocity_list = []
        self.sistem_acceleration_list = []

    
    # старт симуляции рботы двигателей
    def run_simulation(self):

        self.time = 0
        def animation(time):

            self.axis_1.clear()
            self.axis_2.clear()
            self.axis_3.clear()

            self.sistem_acceleration_list.append(self.acceleration)
            self.sistem_velocity_list.append(self.velocity)
            self.sistem_position_list.append(self.position)
            
            self.axis_1.plot(self.sistem_position_list, color="blue", label="position info")
            self.axis_2.plot(self.sistem_velocity_list, color="green", label="velocity info")
            self.axis_3.plot(self.sistem_acceleration_list, color="red", label="acceleration info")

            self.calculate_U_PID(curent_sistem_position=self.position)
            self.general_calculations()
            self.time += self.dt

        self.demo_simulation = FuncAnimation(self.figure, animation, interval=self.simulation_episodes)
        
        self.axis_1.legend(loc="upper left")
        self.axis_2.legend(loc="upper left")
        self.axis_3.legend(loc="upper left")
        
        plt.show()

        self.sistem_acceleration_list = np.asarray(self.sistem_acceleration_list)
        self.sistem_velocity_list = np.asarray(self.sistem_velocity_list)
        self.sistem_position_list = np.asarray(self.sistem_position_list)
    
        return np.array([self.sistem_acceleration_list, self.sistem_velocity_list, self.sistem_position_list])
    




k_p = 150
k_i = 12.9898
k_d = 30
dt = 0.01
T_end = 150
mass = 0.6
B = 3.9865e-08
motor_spid_limit = 10000

sim = Sistem_Sumulation(K_i=k_i, K_d=k_d, K_p=k_p, sat_limit=motor_spid_limit, simulation_episodes=T_end, copter_mass=mass, B=B, position=0, 
                        velocity=0, acceleration=0, rotor_count=4, dt=dt)
sim.set_disired_position(2)
cores = sim.run_simulation()



            






    




        
        

        