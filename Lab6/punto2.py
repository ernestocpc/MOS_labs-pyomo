"""
Laboratorio 6 - Punto 2

Maria Alejandra Estrada - 202021060
Ernesto Carlos Perez - 202112530
"""
import random

coords = [(0,0) ,(0, 80), (20, 60), (40, 20), (40,0)]


def funcion_objetivo(x, y):
    return (3*x+ 2*y)

def simplex(coords):
    # Seleccionar un punto aleatorio
    random_coords = random.randint(0, 4)
    max_fev = None
    fev_actual = 0

    while max_fev != fev_actual:
        # Fev actual y vecinos
        x = coords[random_coords][0]
        y = coords[random_coords][1]
        fev_actual = funcion_objetivo(x, y)

        x_vecino1 = coords[random_coords-1][0]
        y_vecino1 = coords[random_coords-1][1]
        fev_vecino1 = funcion_objetivo(x_vecino1, y_vecino1)

        x_vecino2 = coords[(random_coords+1)%5][0]
        y_vecino2 = coords[(random_coords+1)%5][1]
        fev_vecino2 = funcion_objetivo(x_vecino2, y_vecino2)

        # Se selecciona el mayor de los 3 puntos y se vuelve a comparar con sus vecinos, si hay uno mayor se cambia. Si es igual se termina y retorna el punto y valor.
        max_fev = max(fev_actual, fev_vecino1, fev_vecino2)
        if max_fev == fev_vecino1:
            random_coords = (random_coords - 1) % 5
        elif max_fev == fev_vecino2:
            random_coords = (random_coords + 1) % 5
    return (x, y, max_fev)

print("--------Algoritmo SIMPLEX---------")
respuesta = simplex(coords)
print("Valor optimo de Z:", respuesta[2], "en el punto x =",respuesta[0], " y =",respuesta[1])