"""
Laboratorio 4 - Punto 1

Maria Alejandra Estrada - 202021060
Ernesto Carlos Perez - 202112530

"""

#Escenario de Optimización de Horarios de Entrada/Salida

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
    tiempo=np.random.normal(base, variabilidad)
    return abs(tiempo)  # Tomar el valor absoluto del tiempo generado

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
def ejecutar_simulacion_horarios(numero_personas, tipo_acceso, duracion_simulacion, capacidad_torniquetes, horarios):
    env = simpy.Environment()
    torniquetes = simpy.Resource(env, capacity=capacidad_torniquetes)
    env.process(llegada_personas(env, numero_personas, torniquetes, tipo_acceso))
    for horario in horarios:
        env.process(abrir_cerrar_torniquetes(env, torniquetes, horario['apertura'], horario['cierre']))
    env.run(until=duracion_simulacion)

# Proceso para abrir y cerrar torniquetes según los horarios especificados
def abrir_cerrar_torniquetes(env, torniquetes, hora_apertura, hora_cierre):
    while True:
        if env.now < hora_apertura:
            print(f'Torniquetes cerrados. Próxima apertura a las {hora_apertura} horas')
            yield env.timeout(hora_apertura - env.now)
        else:
            print(f'Torniquetes abiertos a las {hora_apertura} horas')
            yield env.timeout(hora_cierre - env.now)
            print(f'Torniquetes cerrados a las {hora_cierre} horas')
            break


if __name__ == "__main__":
    # Ejemplo de optimización de horarios de entrada/salida con capacidad original de 3 y horarios de apertura/cierre especificados
    horarios = [{'apertura': 8, 'cierre': 17}, {'apertura': 17, 'cierre': 22}]  # Ejemplo de horarios de 8:00 a 17:00 y de 17:00 a 22:00
    ejecutar_simulacion_horarios(numero_personas=300, tipo_acceso='Normal', duracion_simulacion=200, capacidad_torniquetes=3, horarios=horarios)
