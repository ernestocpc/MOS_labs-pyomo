# -*- coding: utf-8 -*-
"""
Laboratorio 5 - Ejercicio 3
Maria Alejandra Estrada - 202021060
Ernesto Carlos Perez - 202112530
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sympy as sp
from sympy.matrices import Matrix

# Inicializar variables simbólicas
x = sp.Symbol('x') #Definir symbolic variables
y = sp.Symbol('y') #Definir symbolic variables

# Definir la función
f = (x - 1)**2 + 100 * (y - x**2)**2

# Calcular las derivadas parciales de la función respecto a x y y
df_dx = sp.diff(f, x)
df_dy = sp.diff(f, y)

# Definir el gradiente como un vector
grad_f = Matrix([df_dx, df_dy])

# Definir la matriz hessiana
hess_f = Matrix([[sp.diff(df, var2) for var2 in (x, y)] for df in grad_f])

# Calcular la inversa de la hessiana
hess_inv = hess_f.inv()

# Inicializar variables
i = 1
norma = 999
alpha = 1

# Inicializar vectores de respuesta
trayec = np.array([[0], [10]])
func = [f.subs({x: trayec[0, 0], y: trayec[1, 0]})]

while norma > 0.001:
    # Evaluar la hessiana en el punto anterior
    a = alpha * np.array(hess_inv.subs({x: trayec[0, i-1], y: trayec[1, i-1]}))
    # Evaluar el gradiente en el punto anterior
    b = np.array([df.subs({x: trayec[0, i-1], y: trayec[1, i-1]}) for df in grad_f])

    # Actualizar los vectores
    new_point = trayec[:, i-1] - np.dot(a, b)
    trayec = np.hstack((trayec, new_point.reshape(2, 1)))
    func.append(f.subs({x: new_point[0], y: new_point[1]}))

    # Calcular condición de parada
    norma = np.linalg.norm(b.astype(float))  # Convertir a float para evitar TypeError

    # Actualizar i
    i += 1

# Mostrar respuesta
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x_vals = np.linspace(-6, 6, 100)
y_vals = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x_vals, y_vals)
Z = (X - 1)**2 + 100 * (Y - X**2)**2

ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.5)

ax.plot_wireframe(X, Y, Z, color='k', alpha=0.5)

ax.scatter(trayec[0, -1], trayec[1, -1], 0, color='r', s=100, label='Mínimo')

ax.plot(trayec[0, :], trayec[1, :], func, color='c', linewidth=8, label='Ruta de puntos encontrados')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('X=X, Y=Y, Z= (X - 1)^2 + 100 (Y - X^2)^2')
plt.legend()
plt.show()
