import numpy as np
import matplotlib.pyplot as  plt
import pandas as pd
 
from matplotlib.animation import FuncAnimation

class COPTER_SISTEM_FILE_DESCRIPTOR():

    def __init__(self, file_type=".xml", serialize_mode=False) -> None:
        
        self.file_type = file_type
        self.serialise_mode = serialize_mode
    
    def create_pandas_data_frame(self, data_dict, n):

        self.dataframe = pd.DataFrame()
        for (item) in data_dict.keys():
            
            if data_dict[item].shape == (n, 3) or data_dict[item].shape == (n, 4):

                for index in range(data_dict[item].shape[1]):
                    self.dataframe[item + f"_[{index}ax]"] = data_dict[item][:, index]

            else:
                self.dataframe[item] = data_dict[item]


    def save_data_in_file(self):
        pass
    
    def save_dataframe_in_csv(self):
        self.dataframe.to_csv("copter_info_files/copter_info.csv")

                    
class COPTER_MECHANIK_MODEL_AND_AUTOMATIC_SISTEM(COPTER_SISTEM_FILE_DESCRIPTOR):

    def __init__(self, B_coeff, target_position, target_velocity, target_acceleration, 
                 copter_mass, Ixx, Iyy, Izz, lenght_of_link, D_coeff, Dt=0.000000001, simulation_steps=100) -> None:
        super().__init__(file_type=".xml", serialize_mode=False)
        self.simulation_step = 1
        self.simulation_epizodes = simulation_steps
        self.B_coeff = B_coeff
        self.copter_mass = copter_mass
        self.lenght_of_link = lenght_of_link
        self.D_coeff = D_coeff
        self.Dt = Dt

        self.copter_position_matrix = np.zeros((self.simulation_epizodes, 3))
        self.copter_velocity_matrix = np.zeros((self.simulation_epizodes, 3))
        self.copter_acceleration_matrix = np.zeros((self.simulation_epizodes, 3))
        self.copter_anguler_velocity_matrix = np.zeros((self.simulation_epizodes, 3))
        self.copter_anguler_acceleration_matrix = np.zeros((self.simulation_epizodes, 3))
        self.copter_theta_angle_matrix = np.zeros(self.simulation_epizodes)
        self.copter_gamma_angle_matrix = np.zeros(self.simulation_epizodes)
        self.copter_psi_angle_matrix = np.zeros(self.simulation_epizodes)
        self.copter_rotors_cmd_matrix = np.zeros((self.simulation_epizodes, 4))

        self.copter_curent_position_vector = np.array([0.0, 0.0, 0.0])
        self.copter_curent_velocity_vector = np.array([0.0, 0.0, 0.0])
        self.copter_curent_acceleration_vector = np.array([0.0, 0.0, 0.0])
        self.copter_curent_anguler_velocity_vector = np.array([0.0, 0.0, 0.0])
        self.copter_curent_anguler_acceleration_vector = np.array([0.0, 0.0, 0.0])
        self.copter_curent_theta_angle = 0.0
        self.copter_curent_gamma_angle = 0.0
        self.copter_curent_psi_angle = 0.0
        self.copter_curent_thrust = 0.0

        self.target_position = target_position
        self.target_velocity = target_velocity
        self.target_acceleration = target_acceleration

        self.pid_desired_position = np.array([0.0, 0.0, 0.0])
        self.pid_desired_velocity = np.array([0.0, 0.0, 0.0])
        self.pid_desired_acceleration = np.array([0.0, 0.0, 0.0])
        self.pid_desired_anguler_velocity = np.array([0.0, 0.0, 0.0])
        self.pid_desired_anguler_acceleration = np.array([0.0, 0.0, 0.0])
        self.pid_desired_theta_angle = 0.0
        self.pid_desired_gamma_angle = 0.0
        self.pid_desired_psi_angle = 6.0

        self.rotors_cmd_list = [1.1, 1.1, 1.1, 1.1]
        self.normalize_vector = np.array([0.0, 0.0, -1.0])
        self.gravitation_vector = np.array([0.0, 0.0, -9.81])

        self.rotation_matrix_3D = np.array([
            [np.cos(self.copter_curent_theta_angle) * np.cos(self.copter_curent_psi_angle), np.cos(self.copter_curent_theta_angle) * np.sin(self.copter_curent_psi_angle), -np.sin(self.copter_curent_theta_angle)],
            [np.sin(self.copter_curent_gamma_angle) * np.sin(self.copter_curent_theta_angle) * np.cos(self.copter_curent_psi_angle) - np.cos(self.copter_curent_gamma_angle) * np.sin(self.copter_curent_psi_angle),
             np.sin(self.copter_curent_gamma_angle) * np.sin(self.copter_curent_theta_angle) * np.sin(self.copter_curent_psi_angle) + np.cos(self.copter_curent_gamma_angle) * np.cos(self.copter_curent_psi_angle),
             np.sin(self.copter_curent_gamma_angle) * np.cos(self.copter_curent_theta_angle)],
             [np.cos(self.copter_curent_gamma_angle) * np.sin(self.copter_curent_theta_angle) * np.cos(self.copter_curent_psi_angle) + np.sin(self.copter_curent_gamma_angle) * np.sin(self.copter_curent_psi_angle),
              np.cos(self.copter_curent_gamma_angle) * np.sin(self.copter_curent_theta_angle) * np.sin(self.copter_curent_psi_angle) - np.sin(self.copter_curent_gamma_angle) * np.cos(self.copter_curent_psi_angle),
              np.cos(self.copter_curent_gamma_angle) * np.cos(self.copter_curent_theta_angle)]
        ])
        self.rotation_matrix_2D = np.array([
            [np.cos(self.copter_curent_gamma_angle), np.sin(self.copter_curent_gamma_angle)],
            [-np.sin(self.copter_curent_theta_angle), np.cos(self.copter_curent_theta_angle)]
        ])

        self.Ixx = Ixx
        self.Iyy = Iyy
        self.Izz = Izz



    
    def calculate_path(self):

        self.trajectory_polinom_matrix = np.array([
            [0, 0, 0, 0, 0, 1],
            [self.simulation_step **  5, self.simulation_step ** 4, self.simulation_step ** 3, self.simulation_step ** 2, self.simulation_step, 1],
            [0, 0, 0, 0, 1, 0],
            [5 * self.simulation_step ** 4, 4 * self.simulation_step ** 3, 3 * self.simulation_step ** 2, 2 * self.simulation_step, 1, 0],
            [0, 0, 0, 2, 0, 0],
            [20 * self.simulation_step ** 3, 12 * self.simulation_step ** 2, 6 * self.simulation_step, 2, 0, 0]
        ])

        self.copter_condition_matrix = np.array([
            [self.copter_curent_position_vector[0], self.target_position[0], self.copter_curent_velocity_vector[0], self.target_velocity[0], self.copter_curent_acceleration_vector[0], self.target_acceleration[0]],
            [self.copter_curent_position_vector[1], self.target_position[1], self.copter_curent_velocity_vector[1], self.target_velocity[1], self.copter_curent_acceleration_vector[1], self.target_acceleration[1]],
            [self.copter_curent_position_vector[2], self.target_position[2], self.copter_curent_velocity_vector[2], self.target_velocity[2], self.copter_curent_acceleration_vector[2], self.target_acceleration[2]]
        ])

        x_coeff = np.linalg.inv(self.trajectory_polinom_matrix).dot(self.copter_condition_matrix[0])
        y_coeff = np.linalg.inv(self.trajectory_polinom_matrix).dot(self.copter_condition_matrix[1])
        z_coeff = np.linalg.inv(self.trajectory_polinom_matrix).dot(self.copter_condition_matrix[2])

        position_x = self.simulation_step ** 5 * x_coeff[0] + self.simulation_step ** 4 * x_coeff[1] + self.simulation_step ** 3 * x_coeff[2] + self.simulation_step ** 2 * x_coeff[3] + self.simulation_step * x_coeff[4] + x_coeff[5]
        position_y = self.simulation_step ** 5 * y_coeff[0] + self.simulation_step ** 4 * y_coeff[1] + self.simulation_step ** 3 * y_coeff[2] + self.simulation_step ** 2 * y_coeff[3] + self.simulation_step * y_coeff[4] + y_coeff[5]
        position_z = self.simulation_step ** 5 * z_coeff[0] + self.simulation_step ** 4 * z_coeff[1] + self.simulation_step ** 3 * z_coeff[2] + self.simulation_step ** 2 * z_coeff[3] + self.simulation_step * z_coeff[4] + z_coeff[5]

        velocity_x = 5 * self.simulation_step ** 4 * x_coeff[0] + 4 * self.simulation_step ** 3 * x_coeff[1] + 3 * self.simulation_step ** 2 * x_coeff[2] + 2 * self.simulation_step * x_coeff[3] + x_coeff[4] 
        velocity_y = 5 * self.simulation_step ** 4 * y_coeff[0] + 4 * self.simulation_step ** 3 * y_coeff[1] + 3 * self.simulation_step ** 2 * y_coeff[2] + 2 * self.simulation_step * y_coeff[3] + y_coeff[4] 
        velocity_z = 5 * self.simulation_step ** 4 * z_coeff[0] + 4 * self.simulation_step ** 3 * z_coeff[1] + 3 * self.simulation_step ** 2 * z_coeff[2] + 2 * self.simulation_step * z_coeff[3] + z_coeff[4] 

        acceleration_x = 20 * self.simulation_step ** 3 * x_coeff[0] + 12 * self.simulation_step ** 2 * x_coeff[1] + 6 * self.simulation_step * x_coeff[2] + x_coeff[3]
        acceleration_y = 20 * self.simulation_step ** 3 * y_coeff[0] + 12 * self.simulation_step ** 2 * y_coeff[1] + 6 * self.simulation_step * y_coeff[2] + y_coeff[3]
        acceleration_z = 20 * self.simulation_step ** 3 * z_coeff[0] + 12 * self.simulation_step ** 2 * z_coeff[1] + 6 * self.simulation_step * z_coeff[2] + z_coeff[3]

        self.pid_desired_position = np.array([position_x, position_y, position_z])
        self.pid_desired_velocity = np.array([velocity_x, velocity_y, velocity_z])
        self.pid_desired_acceleration = np.array([acceleration_x, acceleration_y, acceleration_z])
    
    def calculate_acceleration(self):

        self.tensor_of_inertia = np.array([
            [self.Ixx, 0, 0],
            [0, self.Iyy, 0],
            [0, 0, self.Izz]
        ])
        self.thrust_moment = np.array([
            self.lenght_of_link * self.B_coeff * (self.rotors_cmd_list[0] ** 2 - self.rotors_cmd_list[2] ** 2),
            self.lenght_of_link * self.B_coeff * (self.rotors_cmd_list[3] ** 2 - self.rotors_cmd_list[1] ** 2),
            self.D_coeff * (self.rotors_cmd_list[3] ** 2 + self.rotors_cmd_list[1] ** 2) - self.rotors_cmd_list[0] ** 2 - self.rotors_cmd_list[2] ** 2
        ])

        self.rotor_cmd_sum = sum(self.rotors_cmd_list)
        self.copter_curent_acceleration_vector = self.rotation_matrix_3D.dot(((self.rotor_cmd_sum * self.B_coeff) / self.copter_mass - self.gravitation_vector))
        self.copter_curent_anguler_acceleration_vector = (self.thrust_moment - np.cross(self.copter_curent_anguler_velocity_vector, np.dot(self.tensor_of_inertia, self.copter_curent_anguler_velocity_vector)))

    def calculate_general_mechanik(self):

        self.copter_curent_velocity_vector += self.copter_curent_acceleration_vector * self.Dt
        self.copter_curent_position_vector += self.copter_curent_acceleration_vector * self.Dt
        print(self.copter_curent_velocity_vector)
        self.copter_curent_anguler_velocity_vector += self.copter_curent_anguler_acceleration_vector * self.Dt
        self.copter_curent_gamma_angle += self.copter_curent_anguler_velocity_vector[0] * self.Dt
        self.copter_curent_theta_angle += self.copter_curent_anguler_velocity_vector[1] * self.Dt
        self.copter_curent_psi_angle += self.copter_curent_anguler_velocity_vector[2] * self.Dt
    


