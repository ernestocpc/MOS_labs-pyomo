# -*- coding: utf-8 -*-
"""
Quiz 5 - Proyecto
Autores: Maria Alejandra Estrada - 202021060
         Ernesto Carlos Perez - 202112530
"""

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
model.E = Param(initialize=1)
model.A = Param(initialize=4)

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
model.multi_objective = Objective(expr=sum(model.X[i, j] * model.P[i, j] for i in model.z for j in model.z), sense=maximize)


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

# Solver
SolverFactory('glpk').solve(model)
model.display()
print("\nFuncion objetivo:", model.multi_objective())