# Importante correr pip install scipy sympy numpy matplotlib antes de ejecutar el código
"""
Autores: Maria Alejandra Estrada - 202021060
         Ernesto Carlos Perez - 202112530
"""

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def plot_graph(puntos_iteracion):
    xs = np.linspace(-10, 10, 100)
    ys = 3 * (xs**3) - 10 * (xs**2) - 56 * xs + 50

    plt.plot(xs, ys)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)

    for punto in puntos_iteracion:
        plt.plot(punto[0], punto[1], "ro", fillstyle="none")
        
        if punto == puntos_iteracion[-1]:
            plt.plot(punto[0], punto[1], "ro")
            
    print(
        "Máximo/Mínimo de la función encontrado en x = ",
        puntos_iteracion[-1][0],
        " con valor de f(x) = ",
        puntos_iteracion[-1][1],
    )
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
            print(puntos_iteracion)
            break

        x_i = x_i - alpha * f_prime_val / f_double_prime_val
        # El ultimo punto es el min/max
        puntos_iteracion.append((round(x_i, 2), round(f.subs(x, x_i), 2)))
    return puntos_iteracion


def main():
    # Funcion
    x = sp.symbols("x")
    f = 3 * x**3 - 10 * x**2 - 56 * x + 50

    # Suposición inicial y alpha
    x_guess = 6
    alpha = 0.7

    # Aplicamos el método de Newton-Raphson
    resultado = newton_raphson_2d(f, x_guess, alpha)
    plot = plot_graph(resultado)


main()
