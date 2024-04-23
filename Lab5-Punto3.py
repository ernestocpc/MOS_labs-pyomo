# -*- coding: utf-8 -*-
"""
Laboratorio 5 - Ejercicio 3
Maria Alejandra Estrada - 202021060
Ernesto Carlos Perez - 202112530
"""

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x_symb = sp.Symbol('x') #Definir symbolic variables
y_symb = sp.Symbol('y') #Definir symbolic variables
z_symb = (x_symb-1)**2 + 100*(y_symb-x_symb**2)**2 #Crear la ecuación symbolic

#Sacado de: Differentiate and integrate symbolic expressions
fun_obs = [sp.diff(z_symb, var) for var in (x_symb, y_symb)]
segunda_d = [[sp.diff(fun, var2) for var2 in (x_symb, y_symb)] for fun in fun_obs]

#Sacado de: How and when to use the lambdify function
z_func = sp.lambdify((x_symb, y_symb), z_symb, 'numpy') 
fun_lamb = [sp.lambdify((x_symb, y_symb), fun, 'numpy') for fun in fun_obs]
der_lamb = [[sp.lambdify((x_symb, y_symb), s, 'numpy') for s in seg_d] for seg_d in segunda_d]

def newton_raphson_3d(inicio_x, inicio_y, alpha=1, tolerancia=0.001):
    punto = [inicio_x, inicio_y]
    puntos_his = [punto]
    while True:
        #Sacado de: Performing mathematical operations on arrays
        funcobv = [fun_lamb(*punto) for fun_lamb in fun_lamb]
        der_inv = np.linalg.inv([[der_lamb(*punto) for der_lamb in seg_d] for seg_d in der_lamb])#Calculate the inverse
        cambiar_x = alpha * np.dot(der_inv, funcobv)
        punto = punto - cambiar_x
        puntos_his.append(punto)
        if np.linalg.norm(funcobv) < tolerancia:
            break
    return punto, puntos_his

inicio_x = 0
inicio_y = 10

minima, puntos_his = newton_raphson_3d(inicio_x, inicio_y)

#Sacado de: Creating linespace and meshgrid
x_valores = np.linspace(-10, 10, 100)
y_valores = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x_valores, y_valores)
Z = (X-1)**2 + 100*(Y-X**2)**2

# Sacado de: https://matplotlib.org/stable/plot_types/3D/surface3d_simple.html#sphx-glr-plot-types-3d-surface3d-simple-py

distancias = np.sqrt(X**2 + Y**2)

normalizado_distancias = (distancias - distancias.min()) / (distancias.max() - distancias.min())

colores = plt.cm.viridis(normalizado_distancias)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X, Y, Z, cmap=plt.cm.viridis, facecolors=colores, alpha=1)

ax.plot_wireframe(X, Y, Z, color='k', alpha=0.5)

ax.scatter(*minima, z_func(*minima), color='red', label='Mínimo')

puntos_hiss = np.array(puntos_his)
ax.plot(puntos_hiss[:, 0], puntos_hiss[:, 1], z_func(*puntos_hiss.T), color='blue', label='Ruta de puntos encontrados')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')


plt.title('Método de Newton-Raphson (3D) para encontrar el mínimo de una superficie')

plt.legend()

plt.show()

