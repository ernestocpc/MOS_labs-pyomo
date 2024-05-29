"""
Laboratorio 4 - Punto 1

Maria Alejandra Estrada - 202021060
Ernesto Carlos Perez - 202112530

"""

#Escenario de Mejora de la Tecnología Utilizada

import simpy
import numpy as np

# Constantes de tiempo para cada actividad con su variabilidad
TORNIQUETE_TIEMPO = 5
TORNIQUETE_VARIABILIDAD = 2
CARNET_TIEMPO = 10
CARNET_VARIABILIDAD = 2
QR_TIEMPO = 20
QR_VARIABILIDAD = 2

# Función para generar tiempos aleatorios dentro de una distribución normal
def generar_tiempo(base, variabilidad):
    return np.random.normal(base, variabilidad)

# Proceso de una persona que usa el torniquete
def usar_torniquete(env, nombre, torniquetes, tipo_acceso):
    print(f'{nombre} llega al torniquete a tiempo {env.now}')
    with torniquetes.request() as request:
        yield request
        print(f'{nombre} empieza a preparar el carnet a tiempo {env.now}')
        yield env.timeout(generar_tiempo(CARNET_TIEMPO, CARNET_VARIABILIDAD))
        
        if tipo_acceso == 'QR':
            print(f'{nombre} empieza la lectura de QR a tiempo {env.now}')
            yield env.timeout(generar_tiempo(QR_TIEMPO, QR_VARIABILIDAD))
        
        print(f'{nombre} pasa por el torniquete a tiempo {env.now}')
        yield env.timeout(generar_tiempo(TORNIQUETE_TIEMPO, TORNIQUETE_VARIABILIDAD))
        print(f'{nombre} ha pasado por el torniquete a tiempo {env.now}')

# Función para generar la llegada de personas
def llegada_personas(env, numero_personas, torniquetes, tipo_acceso):
    for i in range(numero_personas):
        env.process(usar_torniquete(env, f'Persona {i}', torniquetes, tipo_acceso))
        yield env.timeout(np.random.exponential(1)) # Llegada de personas de forma exponencial

# Crear el ambiente de SimPy y ejecutar la simulación
def ejecutar_simulacion_mejora_tecnologia(numero_personas, tipo_acceso, duracion_simulacion, capacidad_torniquetes, velocidad_lectura):
    env = simpy.Environment()
    torniquetes = simpy.Resource(env, capacity=capacidad_torniquetes)
    env.process(llegada_personas(env, numero_personas, torniquetes, tipo_acceso))
    env.process(mejorar_lectores_QR(env, velocidad_lectura))
    env.run(until=duracion_simulacion)

# Proceso para mejorar la velocidad de los lectores de QR
def mejorar_lectores_QR(env, velocidad_lectura):
    while True:
        print(f'Mejorando velocidad de los lectores de QR a {velocidad_lectura} unidades por segundo')
        yield env.timeout(30)  # Tiempo de mejora de 30 segundos
        print('Velocidad de los lectores de QR mejorada')

if __name__ == "__main__":
    # Ejemplo de mejora de tecnología con capacidad original de 3 y velocidad de lectura de 50 unidades por segundo
    ejecutar_simulacion_mejora_tecnologia(numero_personas=300, tipo_acceso='QR', duracion_simulacion=200, capacidad_torniquetes=3, velocidad_lectura=50)
