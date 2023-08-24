import numpy as np
import matplotlib.pyplot as plt
from copter_auto_sistem import COPTER_AUTO_SISTEM
from matplotlib.animation import FuncAnimation

#=========================================
class COPTER_SIMULATOR(COPTER_AUTO_SISTEM):

    def __init__(self, B_coeff, target_position, target_velocity, target_acceleration, copter_mass, Ixx, Iyy, Izz, lenght_of_link, D_coeff, Dt=0.01, K_i=0.02, K_d=0.02, K_p=0.02) -> None:
        super().__init__(B_coeff, target_position, target_velocity, target_acceleration, copter_mass, Ixx, Iyy, Izz, lenght_of_link, D_coeff, Dt, K_i, K_d, K_p)

        self.figure = plt.figure()
        self.view_3d = self.figure.add_subplot(projection="3d")
    
    def run_simulation(self):

        while self.simulation_step < self.simulation_epizodes:

            self.calculate_path()
            self.calculate_acceleration()
            self.calculate_general_mechanik()
            self.calculate_desired_copter_thrust_theta_gamma()
            self.calculate_desired_anguler_vel()
            self.calculate_desired_anguler_acc()
            self.calculate_rotors_cmd()

            self.copter_position_matrix[self.simulation_step] = self.copter_curent_position_vector
            self.copter_velocity_matrix[self.simulation_step] = self.copter_curent_velocity_vector
            self.copter_acceleration_matrix[self.simulation_step] = self.copter_curent_acceleration_vector
            self.copter_anguler_velocity_matrix[self.simulation_step] = self.copter_curent_anguler_velocity_vector
            self.copter_anguler_acceleration_matrix[self.simulation_step] = self.copter_curent_anguler_acceleration_vector
            self.copter_theta_angle_matrix[self.simulation_step] = self.copter_curent_theta_angle
            self.copter_gamma_angle_matrix[self.simulation_step] = self.copter_curent_gamma_angle
            self.copter_psi_angle_matrix[self.simulation_step] = self.copter_curent_psi_angle
            self.copter_rotors_cmd_matrix[self.simulation_step] = np.array([self.rotors_cmd_list[0], self.rotors_cmd_list[1], self.rotors_cmd_list[2], self.rotors_cmd_list[3]])

            self.simulation_step += 1
        
        def animation(time):

            self.view_3d.clear()
            self.view_3d.plot(self.copter_position_matrix[0:time, 0], self.copter_position_matrix[0:time, 1], self.copter_position_matrix[0:time, 2], color="gray", alpha=0.3, linestyle="--")
            self.view_3d.quiver(self.copter_position_matrix[time, 0], self.copter_position_matrix[time, 1], self.copter_position_matrix[time, 2],
                              self.copter_velocity_matrix[time, 0], self.copter_velocity_matrix[time, 1], self.copter_velocity_matrix[time, 2], color="red", alpha=0.3)
            self.view_3d.quiver(self.copter_position_matrix[time, 0], self.copter_position_matrix[time, 1], self.copter_position_matrix[time, 2],
                             self.copter_acceleration_matrix[time, 0], self.copter_acceleration_matrix[time, 1], self.copter_acceleration_matrix[time, 2], color="green", alpha=0.3)

        demo = FuncAnimation(self.figure, animation, interval=100)
        plt.show()

        self.data_inf_dict = {"anguler_vel": self.copter_anguler_velocity_matrix, "anguler_acc": self.copter_anguler_acceleration_matrix, "position_vec": self.copter_position_matrix, "linear_vel": self.copter_velocity_matrix, "linear_acc": self.copter_acceleration_matrix,
                              "theta_ang": self.copter_theta_angle_matrix, "gamma_ang": self.copter_gamma_angle_matrix, "psi_ang": self.copter_psi_angle_matrix, "rotors_cmd": self.copter_rotors_cmd_matrix}
        self.create_pandas_data_frame(self.data_inf_dict, self.simulation_epizodes)
        self.save_dataframe_in_csv()
        self.save_data_in_file()
            
if __name__ == "__main__":
    
    target_pos = np.array([12, 15, 16])
    target_vel = np.random.normal(6, 1.2345, 3)
    target_acc = np.random.normal(12, 1.2345, 3)


    obj =  COPTER_SIMULATOR(B_coeff=6.98787867,target_position=target_pos, target_velocity=target_vel,
                            target_acceleration=target_acc, copter_mass=1.006, Ixx=5.6285700000003e-05,
                            Iyy=7.10014300000003e-05, Izz=0.800001000000e-05, lenght_of_link=15, D_coeff=7.00003)
    obj.run_simulation()