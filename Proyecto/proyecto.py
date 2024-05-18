# -- coding: utf-8 --
"""
Proyecto - Escenario 1
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
model.Y = Var(model.z, model.z, model.k, domain=PositiveReals) 

# Función objetivo
model.multi_objective = Objective(expr=sum(model.Y[i, j, k] * model.P[i, j] for i in model.z for j in model.z for k in model.k), sense=maximize)

# Restricción 1: No se pueden asignar más doctores a una zona que el total
# de doctores que están disponibles para el hospital, indicados en los parámetros
# iniciales.
def restriccion1_rule(model, k):
    if k == 'd':
        return sum(model.Y[i, j, k] for i in model.z for j in model.z) <= model.D
    else:
        return Constraint.Skip
model.restriccion1 = Constraint(model.k, rule=restriccion1_rule)

# Restricción 2: No se pueden asignar más enfermeras a una zona que el total
# de enfermeras que están disponibles para el hospital, indicados en los parámetros
# iniciales.
def restriccion2_rule(model, k):
    if k == 'e':
        return sum(model.Y[i, j, k] for i in model.z for j in model.z) <= model.E
    else:
        return Constraint.Skip
model.restriccion2 = Constraint(model.k, rule=restriccion2_rule)

# Restricción 3: No se pueden asignar más administradores a una zona que el total
# de doctores que están disponibles para el hospital, indicados en los parámetros
# iniciales.
def restriccion3_rule(model, k):
    if k == 'a':
        return sum(model.Y[i, j, k] for i in model.z for j in model.z) <= model.A
    else:
        return Constraint.Skip
model.restriccion3 = Constraint(model.k, rule=restriccion3_rule)

# Restricción 4: Solo se pueden asignar doctores donde se requieran
def restriccion4_rule(model, i, j):
    return model.Y[i, j, 'd'] <= model.numD[i, j]
model.restriccion4 = Constraint(model.z, model.z, rule=restriccion4_rule)

# Restricción 5: Solo se pueden asignar enfermeras donde se requieran
def restriccion5_rule(model, i, j):
    return model.Y[i, j, 'e'] <= model.numE[i, j]
model.restriccion5 = Constraint(model.z, model.z, rule=restriccion5_rule)

# Restricción 6: Solo se pueden asignar administradores donde se requieran
def restriccion6_rule(model, i, j):
    return model.Y[i, j, 'a'] <= model.numA[i, j]
model.restriccion6 = Constraint(model.z, model.z, rule=restriccion6_rule)

# Solver
SolverFactory('glpk').solve(model)
model.display()
print("\nFuncion objetivo:", model.multi_objective())