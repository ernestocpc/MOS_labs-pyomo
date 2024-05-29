"""
Laboratorio 4 - Punto 1

Maria Alejandra Estrada - 202021060
Ernesto Carlos Perez - 202112530
"""

"""
´Paso 1: Codificar el Proceso Básico del Torniquete:

- Desarrollaremos el código en Python utilizando SimPy para modelar el proceso básico de los torniquetes.
- Capturaremos todos los componentes y flujos de proceso descritos, incluyendo la llegada de personas, la preparación del carnet y el paso por el torniquete.
"""

"""
Paso 2: Integrar Variabilidad
- Utilizamos np.random.normal para agregar variabilidad a los tiempos de las actividades.
- Cada tiempo se calcula con una media y una desviación estándar.

Paso 3: Asegurar la Precisión
- Comparamos los resultados de la simulación con los datos reales del edificio Santo Domingo.
- Validamos y refinamos el código según sea necesario.
"""

import simpy
import numpy as np

# Definimos las constantes de tiempo para cada actividad con su variabilidad
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
def ejecutar_simulacion():
    env = simpy.Environment()
    torniquetes = simpy.Resource(env, capacity=3)
    env.process(llegada_personas(env, 100, torniquetes, tipo_acceso='Normal'))
    env.process(llegada_personas(env, 10, torniquetes, tipo_acceso='QR'))
    env.run(until=100) # Simular por 100 unidades de tiempo

if __name__ == "__main__":
    ejecutar_simulacion()


