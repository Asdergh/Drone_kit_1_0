import numpy as np
from copter_math_model import COPTER_MECHANIK_MODEL_AND_AUTOMATIC_SISTEM


class COPTER_AUTO_SISTEM(COPTER_MECHANIK_MODEL_AND_AUTOMATIC_SISTEM):

    def __init__(self, B_coeff, target_position, target_velocity, target_acceleration, copter_mass, Ixx, Iyy, Izz, lenght_of_link, D_coeff, Dt=0.01, K_i = 1.02, K_d = 2.02, K_p = 1.02) -> None:
        super().__init__(B_coeff, target_position, target_velocity, target_acceleration, copter_mass, Ixx, Iyy, Izz, lenght_of_link, D_coeff, Dt)
        
        self.K_i = K_i
        self.K_d =  K_d
        self.K_p = K_p

        self.pid_integr_pos_z = 0.0
        self.pid_integr_pos_y = 0.0
        self.pid_integr_pos_x = 0.0

        self.pid_integr_anguler_vel_x = 0.0
        self.pid_integr_anguler_vel_y = 0.0
        self.pid_integr_anguler_vel_z = 0.0

        self.pid_integr_theta = 0.0
        self.pid_integr_gamma = 0.0
        self.pid_integr_psi = 0.0

        self.pid_past_position_error_x = 0.0
        self.pid_past_position_error_y = 0.0
        self.pid_past_position_error_z = 0.0

        self.pid_anguler_vel_past_error_x = 0.0
        self.pid_anguler_vel_past_error_y = 0.0
        self.pid_anguler_vel_past_error_z = 0.0

        self.pid_theta_past_error = 0.0
        self.pid_gamma_past_error = 0.0
        self.pid_psi_past_error = 0.0

    

    def calculate_desired_copter_thrust_theta_gamma(self):

        self.copter_position_z = self.pid_desired_position[2] - self.copter_curent_position_vector[2]
        self.copter_position_y = self.pid_desired_position[1] - self.copter_curent_position_vector[1]
        self.copter_position_x = self.pid_desired_position[0] - self.copter_curent_position_vector[0]

        self.pid_integr_pos_z += self.copter_position_z * self.Dt
        self.pid_integr_pos_y += self.copter_position_y * self.Dt
        self.pid_integr_pos_x += self.copter_position_x * self.Dt

        self.copter_curent_thrust = self.K_p * self.copter_position_z + self.K_i * self.pid_integr_pos_z + self.K_d * (self.copter_position_z - self.pid_past_position_error_z) / self.Dt
        self.pid_desired_theta_angle = self.K_p * self.copter_position_y + self.K_i * self.pid_integr_theta + self.K_d * (self.copter_position_y - self.pid_past_position_error_y) / self.Dt
        self.pid_desired_gamma_angle = self.K_p * self.copter_position_x + self.K_i * self.pid_integr_gamma + self.K_d * (self.copter_position_x - self.pid_past_position_error_x) / self.Dt

        self.pid_past_position_error_z = self.copter_position_z
        self.pid_past_position_error_y = self.copter_position_y
        self.pid_past_position_error_x = self.copter_position_x

    def calculate_desired_anguler_vel(self):

        self.copter_theta_error = self.pid_desired_theta_angle - self.copter_curent_theta_angle
        self.copter_gamma_error = self.pid_desired_gamma_angle - self.copter_curent_theta_angle
        self.copter_psi_error = self.pid_desired_psi_angle - self.copter_curent_psi_angle

        self.pid_integr_theta = self.copter_theta_error * self.Dt
        self.pid_integr_gamma = self.copter_gamma_error * self.Dt
        self.pid_integr_psi = self.copter_psi_error * self.Dt

        self.pid_desired_anguler_velocity[0] = self.K_p * self.copter_theta_error + self.K_i * self.pid_integr_theta + self.K_d * (self.copter_theta_error - self.pid_theta_past_error) / self.Dt
        self.pid_desired_anguler_velocity[1] = self.K_p * self.copter_gamma_error + self.K_i * self.pid_integr_gamma + self.K_d * (self.copter_gamma_error - self.pid_gamma_past_error) / self.Dt
        self.pid_desired_anguler_velocity[2] = self.K_p * self.copter_psi_error + self.K_i * self.pid_integr_psi + self.K_d * (self.copter_psi_error - self.pid_psi_past_error) / self.Dt

        self.pid_theta_past_error = self.copter_theta_error
        self.pid_gamma_past_error = self.copter_gamma_error
        self.pid_psi_past_error = self.copter_psi_error
    
    def calculate_desired_anguler_acc(self):

        self.copter_anguler_vel_error_x = self.pid_desired_anguler_velocity[0] - self.copter_curent_anguler_velocity_vector[0]
        self.copter_anguler_vel_error_y = self.pid_desired_anguler_velocity[1] - self.copter_curent_anguler_velocity_vector[1]
        self.copter_anguler_vel_error_z = self.pid_desired_anguler_velocity[2] - self.copter_curent_anguler_velocity_vector[2]

        self.pid_integr_anguler_vel_x = self.copter_anguler_vel_error_x * self.Dt
        self.pid_integr_anguler_vel_y = self.copter_anguler_vel_error_y * self.Dt
        self.pid_integr_anguler_vel_z = self.copter_anguler_vel_error_z * self.Dt

        self.pid_desired_anguler_acceleration[0] = self.K_p * self.copter_anguler_vel_error_x + self.K_i * self.pid_integr_anguler_vel_x + self.K_d * (self.copter_anguler_vel_error_x - self.pid_anguler_vel_past_error_x) / self.Dt
        self.pid_desired_anguler_acceleration[1] = self.K_p * self.copter_anguler_vel_error_y + self.K_i * self.pid_integr_anguler_vel_y + self.K_d * (self.copter_anguler_vel_error_y - self.pid_anguler_vel_past_error_y) / self.Dt
        self.pid_desired_anguler_acceleration[2] = self.K_p * self.copter_anguler_vel_error_z + self.K_i * self.pid_integr_anguler_vel_z + self.K_d * (self.copter_anguler_vel_error_z - self.pid_anguler_vel_past_error_z) / self.Dt

        self.pid_anguler_vel_past_error_x = self.copter_anguler_vel_error_x
        self.pid_anguler_vel_past_error_y = self.copter_anguler_vel_error_y
        self.pid_anguler_vel_past_error_z = self.copter_anguler_vel_error_z
    
    def calculate_rotors_cmd(self):

        self.rotors_cmd_list[0] = self.copter_curent_thrust - self.pid_desired_anguler_acceleration[2] + self.pid_desired_anguler_acceleration[0]
        self.rotors_cmd_list[1] = self.copter_curent_thrust + self.pid_desired_anguler_acceleration[2] - self.pid_desired_anguler_acceleration[1]
        self.rotors_cmd_list[2] = self.copter_curent_thrust - self.pid_desired_anguler_acceleration[2] - self.pid_desired_anguler_acceleration[0]
        self.rotors_cmd_list[3] = self.copter_curent_thrust + self.pid_desired_anguler_acceleration[2] + self.pid_desired_anguler_acceleration[1]
    
