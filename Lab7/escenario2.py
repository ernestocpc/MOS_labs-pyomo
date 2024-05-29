"""
Laboratorio 4 - Punto 1

Maria Alejandra Estrada - 202021060
Ernesto Carlos Perez - 202112530

En este escenario, evaluamos el impacto de aumentar la velocidad de los lectores de QR en el sistema de torniquetes. 
El objetivo es simular diferentes velocidades de procesamiento para los lectores de QR y analizar su efecto en el 
tiempo total de espera y la eficiencia del sistema.

El código escenario2.py se encarga de simular este escenario. Se ajusta la velocidad de procesamiento de los lectores 
de QR y se ejecuta la simulación para observar cómo cambian los tiempos de espera y la eficiencia del sistema.

"""

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
    tiempo_generado = np.random.normal(base, variabilidad)
    return abs(tiempo_generado)  # Tomar el valor absoluto del tiempo generado

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
def ejecutar_simulacion(numero_personas, tipo_acceso, duracion_simulacion):
    env = simpy.Environment()
    torniquetes = simpy.Resource(env, capacity=3)
    env.process(llegada_personas(env, numero_personas, torniquetes, tipo_acceso))
    env.run(until=duracion_simulacion)

if __name__ == "__main__":
    ejecutar_simulacion(numero_personas=100, tipo_acceso='QR', duracion_simulacion=100)
