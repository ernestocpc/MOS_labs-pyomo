"""
Autores: Maria Alejandra Estrada - 202021060
         Ernesto Carlos Perez - 202112530
"""
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

def plot_graph():
    xs = np.linspace(-3, 3, 100)
    ys = (xs**5) -  8*(xs**3) + 10*(xs) + 6

    plt.plot(xs, ys)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)

    plt.show()


def newton_raphson_intervalo(f, x_min, x_max, alpha, convergence=0.001):
    x = sp.symbols("x")

    f_prime = sp.diff(f, x) # Primera derivada: 5x^4 - 24x^2 + 10
    f_double_prime = sp.diff(f_prime, x) # Segunda derivada: 20x^3 - 48x

    # Sacar puntos a evaluar
    x_values = np.linspace(x_min, x_max, 100)
    max_min_posibles = []



    for x_i in x_values:
        f_prime_val = f_prime.subs(x, x_i)
        f_double_prime_val = f_double_prime.subs(x, x_i)

        if abs(f_prime_val) < convergence:
            max_min_posibles.append((round(x_i, 2), round(f.subs(x, x_i), 2)))


        # Como converger??
        x_new = x_i - alpha * f_prime_val / f_double_prime_val
        print(x_i, x_new)
        if x_new >= x_min and x_new <= x_max:
            x_i = x_new

    return max_min_posibles


def main():
    # Funcion
    x = sp.symbols("x")
    f = x**5 - 8*x**3 + 10*x + 6

    # Suposición inicial y alpha
    x_min = -3
    x_max = 3
    alpha = 0.5

    # Aplicamos el método de Newton-Raphson
    resultado = newton_raphson_intervalo(f, x_min, x_max, alpha)
    print(resultado)
    # plot = plot_graph(resultado)


main()
