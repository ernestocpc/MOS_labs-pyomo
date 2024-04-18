# Importante correr pip install scipy sympy numpy matplotlib antes de ejecutar el código
"""
Autores: Maria Alejandra Estrada - 202021060
         Ernesto Carlos Perez - 202112530
"""

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def plot_graph(puntos_iteracion1, puntos_iteracion2, puntos_iteracion3):
    xs = np.linspace(-6, 6, 100)
    ys = 3 * (xs**3) - 10 * (xs**2) - 56 * xs + 50

    plt.plot(xs, ys)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)

    # Rojo para para -6 y alpha 0.6
    for punto in puntos_iteracion1:
        plt.plot(punto[0], punto[1], "ro", fillstyle="none")
        
        if punto == puntos_iteracion1[-1]:
            plt.plot(punto[0], punto[1], "ro")

    # Cyan para para 6 y alpha 0.6
    for punto in puntos_iteracion2:
        plt.plot(punto[0], punto[1], "co", fillstyle="none")
        
        if punto == puntos_iteracion2[-1]:
            plt.plot(punto[0], punto[1], "co")

    # Verde para para -6 y alpha 1
    for punto in puntos_iteracion3:
        plt.plot(punto[0], punto[1], "go", fillstyle="none")
        
        if punto == puntos_iteracion3[-1]:
            plt.plot(punto[0], punto[1], "go")
        
    # Agregar leyenda
    legend_colors = ['black', 'red', 'cyan', 'green']

    plt.legend(["f(x) = 3x^3 - 10x^2 - 56x + 50", "x = -6, alpha = 0.6", "x = 6, alpha = 0.6", "x = -6, alpha = 1"],
               labelcolor=legend_colors)

    plt.show()


def newton_raphson_2d(f, x_guess, alpha, convergence=0.001):
    x = sp.symbols("x")
    f_prime = sp.diff(f, x)
    f_double_prime = sp.diff(f_prime, x)

    x_i = x_guess

    puntos_iteracion = []

    while True:
        f_prime_val = f_prime.subs(x, x_i)
        f_double_prime_val = f_double_prime.subs(x, x_i)

        if abs(f_prime_val) < convergence:
            break

        x_i = x_i - alpha * f_prime_val / f_double_prime_val
        # El ultimo punto es el min/max
        puntos_iteracion.append((round(x_i, 2), round(f.subs(x, x_i), 2)))
    return puntos_iteracion


def main():
    # Funcion
    x = sp.symbols("x")
    f = 3 * x**3 - 10 * x**2 - 56 * x + 50


    # Aplicamos el método de Newton-Raphson
    resultado1 = newton_raphson_2d(f, -6, 0.6)
    resultado2 = newton_raphson_2d(f, 6, 0.6)
    resultado3 = newton_raphson_2d(f, -6, 1)
    plot = plot_graph(resultado1, resultado2, resultado3)


main()
