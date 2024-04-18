"""
Autores: Maria Alejandra Estrada - 202021060
         Ernesto Carlos Perez - 202112530
"""
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

def plot_graph(puntos):
    xs = np.linspace(-3, 3, 100)
    ys = (xs**5) -  8*(xs**3) + 10*(xs) + 6

    plt.plot(xs, ys)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)

    for punto in puntos:

        if punto == puntos[0]:
            plt.plot(punto[0], punto[1], "ro")

        elif punto == puntos[-1]:
            plt.plot(punto[0], punto[1], "ro")

        else:
            # Show the dot black
            plt.plot(punto[0], punto[1], "ko")

    legend_colors = ['black', 'black' , 'red']
    plt.legend(["f(x) = x^5 - 8x^3 + 10x + 6", "Máximos y mínimos globales", "Máximos y mínimos locales"],)
        
    plt.show()


def newton_raphson_2d(f, x_guess, alpha, convergence=0.001):
    x = sp.symbols("x")
    f_prime = sp.diff(f, x)
    f_double_prime = sp.diff(f_prime, x)

    x_i = x_guess

    while True:
        f_prime_val = f_prime.subs(x, x_i)
        f_double_prime_val = f_double_prime.subs(x, x_i)

        if abs(f_prime_val) < convergence:
            break

        x_i = x_i - alpha * f_prime_val / f_double_prime_val
    return round(x_i, 2), round(f.subs(x, x_i), 2)


def main():
    # Funcion
    x = sp.symbols("x")
    f = x**5 - 8*x**3 + 10*x + 6


    x_values = np.linspace(-3, 3, 10)
    puntos_min_max = []
    for x_guess in x_values:
        resultado = newton_raphson_2d(f, x_guess, 1)
        if resultado not in puntos_min_max:
            puntos_min_max.append(resultado)

    puntos_min_max.sort(key=lambda x: x[0])
    plot_graph(puntos_min_max)


main()
