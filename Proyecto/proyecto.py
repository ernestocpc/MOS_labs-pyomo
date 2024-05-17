# -*- coding: utf-8 -*-
"""
Quiz 5 - Proyecto
Autores: Maria Alejandra Estrada - 202021060
         Ernesto Carlos Perez - 202112530
"""
# Respuesta Correcta = 17
# Importaciones
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Creación modelo
model = ConcreteModel()

# Conjuntos
model.z = Set(initialize=['p1', 'p2', 'p3'])
model.k = Set(initialize=['d', 'e', 'a'])

# Parametros
model.D = Param(initialize=2)
model.A = Param(initialize=1)
model.E = Param(initialize=4)

prioridades = {
    ('p1', 'p1'): 5, ('p1', 'p2'): 2, ('p1', 'p3'): 0.01,
    ('p2', 'p1'): 3, ('p2', 'p2'): 2, ('p2', 'p3'): 0.01,  
    ('p3', 'p1'): 3, ('p3', 'p2'): 5, ('p3', 'p3'): 0.01 
}
model.P = Param(model.z, model.z, initialize=prioridades)

doctores = {
    ('p1', 'p1'): 2, ('p1', 'p2'): 0, ('p1', 'p3'): 0,
    ('p2', 'p1'): 0, ('p2', 'p2'): 0, ('p2', 'p3'): 0,
    ('p3', 'p1'): 1, ('p3', 'p2'): 0, ('p3', 'p3'): 0
} 
model.numD = Param(model.z, model.z, initialize=doctores)

enfermeras = {
    ('p1', 'p1'): 0, ('p1', 'p2'): 2, ('p1', 'p3'): 1,
    ('p2', 'p1'): 2, ('p2', 'p2'): 2, ('p2', 'p3'): 1,
    ('p3', 'p1'): 0, ('p3', 'p2'): 0, ('p3', 'p3'): 0
}
model.numE = Param(model.z, model.z, initialize=enfermeras)

administradores = {
    ('p1', 'p1'): 0, ('p1', 'p2'): 0, ('p1', 'p3'): 0,
    ('p2', 'p1'): 0, ('p2', 'p2'): 0, ('p2', 'p3'): 0,
    ('p3', 'p1'): 0, ('p3', 'p2'): 1, ('p3', 'p3'): 1
}
model.numA = Param(model.z, model.z, initialize=administradores) 

# Variables de decisión
model.X = Var(model.z, model.z, domain=Binary)  
model.Y = Var(model.z, model.z, model.k, domain=PositiveReals) 

# Función objetivo
"""
La Función Objetivo busca maximizar las zonas cubiertas seg ́un su prioridad
por el personal necesario. Dado que se usa un sistema de prioridad donde 1 es
minimo y 5 es maximo el algoritmo va a priorizar cubrir zonas con alta prioridad.
"""
#model.multi_objective = Objective(expr=sum(model.X[i, j] * model.P[i, j] for i in model.z for j in model.z), sense=maximize)

model.multi_objective = Objective(expr=sum(model.Y[i, j, k] * model.P[i, j] for i in model.z for j in model.z for k in model.k), sense=maximize)


"""
Restriccion 1: Los doctores que est ́an ubicados en una zona ofrecen cobertura
 ́unicamente a las zonas adyacentes de su posici ́on.
"""

"""
@Mariale -> ESTA ES LA QUE FALTA
def restriccion1_rule(model, i, j, k):
    if k == 'd':
        if i == 'p1' and j == 'p2':
            return model.Y[i, j, k] <= model.numD[i, j]
        elif i == 'p1' and j == 'p3':
            return model.Y[i, j, k] <= model.numD[i, j]
        elif i == 'p2' and j == 'p1':
            return model.Y[i, j, k] <= model.numD[i, j]
        elif i == 'p2' and j == 'p3':
            return model.Y[i, j, k] <= model.numD[i, j]
        elif i == 'p3' and j == 'p1':
            return model.Y[i, j, k] <= model.numD[i, j]
        elif i == 'p3' and j == 'p2':
            return model.Y[i, j, k] <= model.numD[i, j]
        else:
            return model.Y[i, j, k] == 0
    else:
        return Constraint.Skip
model.restriccion1 = Constraint(model.z, model.z, model.k, rule=restriccion1_rule)
"""

"""
Restriccion 2: No se pueden asignar más doctores a una zona que el total
de doctores que están disponibles para el hospital, indicados en los parámetros
iniciales.

"""
def restriccion2_rule(model, k):
    if k == 'd':
        return sum(model.Y[i, j, k] for i in model.z for j in model.z) <= model.D
    else:
        return Constraint.Skip
model.restriccion2 = Constraint(model.k, rule=restriccion2_rule)

"""
Restriccion 3: No se pueden asignar m as enfermeras a una zona que el total
de enfermeras que est ́an disponibles para el hospital, indicados en los par ́ametros
iniciales.

"""
def restriccion3_rule(model, k):
    if k == 'e':
        return sum(model.Y[i, j, k] for i in model.z for j in model.z) <= model.E
    else:
        return Constraint.Skip
model.restriccion3 = Constraint(model.k, rule=restriccion3_rule)


"""
Restriccion 4: No se pueden asignar m as administradores a una zona que el to-
tal de doctores que est ́an disponibles para el hospital, indicados en los par ́ametros
iniciales.
"""
def restriccion4_rule(model, k):
    if k == 'a':
        return sum(model.Y[i, j, k] for i in model.z for j in model.z) <= model.A
    else:
        return Constraint.Skip
model.restriccion4 = Constraint(model.k, rule=restriccion4_rule)

"""
Restriccion 5: Relacionar variable X y Y 
"""
def restriccion5_rule(model, i, j):
   return sum(model.Y[i,j,k] for k in model.k) <= model.X[i,j] * 100000000

model.restriccion5 = Constraint(model.z, model.z, rule=restriccion5_rule)

"""
Restricción 6: Solo se pueden asignar doctores donde se requieran
"""
def restriccion6_rule(model, i, j):
    return model.Y[i, j, 'd'] <= model.numD[i, j]

model.restriccion6 = Constraint(model.z, model.z, rule=restriccion6_rule)

"""
Restricción 7: Solo se pueden asignar enfermeras donde se requieran
"""
def restriccion7_rule(model, i, j):
    return model.Y[i, j, 'e'] <= model.numE[i, j]

model.restriccion7 = Constraint(model.z, model.z, rule=restriccion7_rule)

"""
Restricción 8: Solo se pueden asignar enfermeras donde se requieran
"""
def restriccion8_rule(model, i, j):
    return model.Y[i, j, 'a'] <= model.numA[i, j]

model.restriccion8 = Constraint(model.z, model.z, rule=restriccion8_rule)

# Solver
SolverFactory('glpk').solve(model)
model.display()
print("\nFuncion objetivo:", model.multi_objective())