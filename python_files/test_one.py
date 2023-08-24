import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def path_calculater(points_array):
                        
    trajectory_time = 0
    trajectory_polinom_result = []
    trajectory_exterpolation_polinom_result = []


    exterpolation_time_matrix = np.array([
        [1, 1, 1, 1],
        [8, 4, 2, 1],
        [27, 9, 3, 1],
        [64, 16, 4, 1]
    ])
    print(exterpolation_time_matrix.shape)
    exterpolation_x_vector = points_array[:, 0]
    exterpolation_y_vector = points_array[:, 1]
    exterpolation_z_vector = points_array[:, 2]

    target_x_coeff_vector = np.linalg.inv(exterpolation_time_matrix).dot(exterpolation_x_vector)
    target_y_coeff_vector = np.linalg.inv(exterpolation_time_matrix).dot(exterpolation_y_vector)
    target_z_coeff_vector = np.linalg.inv(exterpolation_time_matrix).dot(exterpolation_z_vector)

    while trajectory_time < 100:
        
        Cx_0 = points_array[0, 0] / ((1 - 2) * (1 - 3) * (1 - 4))
        Cx_1 = points_array[1, 0] / ((2 - 1) * (2 - 3) * (2 - 4))
        Cx_2 = points_array[2, 0] / ((3 - 1) * (3 - 2) * (3 - 4))
        Cx_3 = points_array[3, 0] / ((4 - 1) * (4 - 2) * (4 - 3))
        
        Cy_0 = points_array[0, 1] / ((1 - 2) * (1 - 3) * (1 - 4))
        Cy_1 = points_array[1, 1] / ((2 - 1) * (2 - 3) * (2 - 4))
        Cy_2 = points_array[2, 1] / ((3 - 1) * (3 - 2) * (3 - 4))
        Cy_3 = points_array[3, 1] / ((4 - 1) * (4 - 2) * (4 - 3))
        
        Cz_0 = points_array[0, 2] / ((1 - 2) * (1 - 3) * (1 - 4))
        Cz_1 = points_array[1, 2] / ((2 - 1) * (2 - 3) * (2 - 4))
        Cz_2 = points_array[2, 2] / ((3 - 1) * (3 - 2) * (3 - 4))
        Cz_3 = points_array[3, 2] / ((4 - 1) * (4 - 2) * (4 - 3))
        
        
        x_polinom_result = (trajectory_time - 2) * (trajectory_time - 3) * (trajectory_time - 4) * Cx_0 + \
                            (trajectory_time - 1) * (trajectory_time - 3) * (trajectory_time - 4) * Cx_1 + \
                            (trajectory_time - 1) * (trajectory_time - 2) * (trajectory_time - 4) * Cx_2 + \
                            (trajectory_time - 1) * (trajectory_time - 2) * (trajectory_time - 3) * Cx_3
                            
        y_polinom_result = (trajectory_time - 2) * (trajectory_time - 3) * (trajectory_time - 4) * Cy_0 + \
                            (trajectory_time - 1) * (trajectory_time - 3) * (trajectory_time - 4) * Cy_1 + \
                            (trajectory_time - 1) * (trajectory_time - 2) * (trajectory_time - 4) * Cy_2 + \
                            (trajectory_time - 1) * (trajectory_time - 2) * (trajectory_time - 3) * Cy_3
        
        z_polinom_result = (trajectory_time - 2) * (trajectory_time - 3) * (trajectory_time - 4) * Cz_0 + \
                            (trajectory_time - 1) * (trajectory_time - 3) * (trajectory_time - 4) * Cz_1 + \
                            (trajectory_time - 1) * (trajectory_time - 2) * (trajectory_time - 4) * Cz_2 + \
                            (trajectory_time - 1) * (trajectory_time - 2) * (trajectory_time - 3) * Cz_3
        
        x_exterpolation_result = target_x_coeff_vector[0] * trajectory_time ** 3 + target_x_coeff_vector[1] * trajectory_time ** 2 + target_x_coeff_vector[2] * trajectory_time + target_x_coeff_vector[3]
        y_exterpolation_result = target_y_coeff_vector[0] * trajectory_time ** 3 + target_y_coeff_vector[1] * trajectory_time ** 2 + target_y_coeff_vector[2] * trajectory_time + target_y_coeff_vector[3]
        z_exterpolation_result = target_z_coeff_vector[0] * trajectory_time ** 3 + target_z_coeff_vector[1] * trajectory_time ** 2 + target_z_coeff_vector[2] * trajectory_time + target_z_coeff_vector[3]
        
        trajectory_exterpolation_polinom_result.append([x_exterpolation_result, y_exterpolation_result, z_exterpolation_result])
        trajectory_polinom_result.append([x_polinom_result, y_polinom_result, z_polinom_result])
        
        trajectory_time += 1


    trajectory_polinom_result = np.array(trajectory_polinom_result)
    trajectory_exterpolation_polinom_result = np.array(trajectory_exterpolation_polinom_result) + np.random.normal(3.45, 0.3456)

    return trajectory_polinom_result, trajectory_exterpolation_polinom_result

figure = plt.figure()
surface = figure.add_subplot(projection="3d")


def animation(time):
    surface.clear()
    cores_matrix = np.array([np.random.normal(10, 5.46, 4),
                    np.random.normal(10, 5.46, 4),
                    np.random.normal(10, 5.46, 4)]).T
    
    result_cores, result_2_cores = path_calculater(points_array=cores_matrix)
    surface.plot(result_cores[:, 0], result_cores[:, 1], result_cores[:, 2], color="red", alpha=0.3)
    surface.plot(result_2_cores[:, 0], result_2_cores[:, 1], result_2_cores[:, 2], color="blue", alpha=0.3, linestyle="--")

demo = FuncAnimation(figure, animation, interval=1000)
plt.show()
