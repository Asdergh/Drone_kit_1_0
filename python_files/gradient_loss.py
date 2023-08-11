import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation



plt.style.use("seaborn")
figure = plt.figure()
axis_3d = figure.add_subplot(projection="3d")

def init_function(x, y):
    return np.cos(np.sqrt(x ** 2 + y ** 2)) * np.sin(np.sqrt(x ** 2 + y ** 2))

def derivative_of_function_x(x, y):
    return (init_function(x + 0.0000001, y) - init_function(x, y)) / 0.0000001

def derivative_of_function_y(x, y):
    return (init_function(x, y + 0.0000001) - init_function(x, y)) / 0.0000001


def gradient_upp(X, Y, Z, eta=0.01):

    X = np.ravel(X)
    Y = np.ravel(Y)
    Z = np.ravel(Z)
    print(Z.shape)
    
    X_point_array = np.zeros(X.shape)
    Y_point_array = np.zeros(Y.shape)

    X_point_array[0] = X[0]
    Y_point_array[1] = Y[0]
    

    for (index, item) in enumerate(Z):

        dir_xx = derivative_of_function_x(X[index] + 0.0000001, Y[index])
        dir_xy = derivative_of_function_x(X[index], Y[index] + 0.0000001)
        dir_yx = derivative_of_function_y(X[index] + 0.0000001, Y[index])
        dir_yy = derivative_of_function_y(X[index], Y[index] + 0.0000001)

        A_1 = dir_xx
        A_2 = dir_xx * dir_yy - dir_xy * dir_yx

        if (A_1 > 0 and A_2 > 0):
            print(f"local min point at point: [X: {X[index]}, Y: {[Y[index]]}, Z: {item}")
        
        elif (A_1 < 0 and A_2 < 0):

            X_point_array[index + 1] = X_point_array[index] - eta * derivative_of_function_x(X[index], Y[index])
            Y_point_array[index + 1] = Y_point_array[index] - eta * derivative_of_function_y(X[index], Y[index])
    
    return X_point_array, Y_point_array, Z


x_grid, y_grid = np.meshgrid(np.linspace(-np.pi, np.pi, 100),
                             np.linspace(-np.pi, np.pi, 100))
z_grid = init_function(x_grid, y_grid)

x, y, z = gradient_upp(x_grid, y_grid, z_grid)
print(x.shape, y.shape, z.shape)
axis_3d.plot_surface(x_grid, y_grid, z_grid, alpha=0.5, lw=0.5, rstride=8, cstride=8, color="gray", edgecolor="blue")
axis_3d.contourf(x_grid, y_grid, z_grid, zdir="z", offset=-1.35, cmap="coolwarm", alpha=0.5)
axis_3d.contour(x_grid, y_grid, z_grid, zdir="z", offset=-1.35, cmap="magma")

axis_3d.plot(x, y, z, linestyle="--", color="black", alpha=0.5)
#axis_3d.plot(x, y, 0, linestyle="--", color="red")


plt.show()




