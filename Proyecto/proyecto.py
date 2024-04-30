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
model.i = Set(initialize=['p1', 'p2', 'p3'])
model.j = Set(initialize=model.i)
model.k = Set(initialize=['d', 'e', 'a'])

# Parametros
model.D = Param(initialize=2)
model.E = Param(initialize=1)
model.A = Param(initialize=4)

prioridades = {
    ('p1', 'p1'): 5, ('p1', 'p2'): 2, ('p1', 'p3'): 0,
    ('p2', 'p1'): 3, ('p2', 'p2'): 2, ('p2', 'p3'): 0,
    ('p3', 'p1'): 3, ('p3', 'p2'): 5, ('p3', 'p3'): 0
}
model.P = Param(model.i, model.j, initialize=prioridades)

doctores = {
    ('p1', 'p1'): 2, ('p1', 'p2'): 0, ('p1', 'p3'): 0,
    ('p2', 'p1'): 0, ('p2', 'p2'): 0, ('p2', 'p3'): 0,
    ('p3', 'p1'): 1, ('p3', 'p2'): 0, ('p3', 'p3'): 0
} 
model.numD = Param(model.i, model.j, initialize=doctores)

enfermeras = {
    ('p1', 'p1'): 0, ('p1', 'p2'): 2, ('p1', 'p3'): 1,
    ('p2', 'p1'): 2, ('p2', 'p2'): 2, ('p2', 'p3'): 1,
    ('p3', 'p1'): 0, ('p3', 'p2'): 0, ('p3', 'p3'): 0
}
model.numE = Param(model.i, model.j, initialize=enfermeras)

administradores = {
    ('p1', 'p1'): 0, ('p1', 'p2'): 0, ('p1', 'p3'): 0,
    ('p2', 'p1'): 0, ('p2', 'p2'): 0, ('p2', 'p3'): 0,
    ('p3', 'p1'): 0, ('p3', 'p2'): 1, ('p3', 'p3'): 1
}
model.numA = Param(model.i, model.j, initialize=administradores) 

# Variables de decisión
model.X = Var(model.i, model.j, domain=Binary)  
model.Y = Var(model.i, model.j, model.k, domain=PositiveReals) 

# Función objetivo
model.multi_objective = Objective(expr=sum(model.X[i, j] * model.P[i, j] for i in model.i for j in model.j), sense=maximize)

# Definir restricciones de inicialización para las variables X
def init_X_rule(model, i, j):
    return model.X[i, j] == 0

# Añadir las restricciones de inicialización al modelo
model.init_X = Constraint(model.i, model.j, rule=init_X_rule)

# Solver
results=SolverFactory('glpk').solve(model)

# Verificar si la solución es válida
if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
    # Mostrar la solución
    model.display()

    # Calcular y mostrar el valor de la función objetivo
    objective_value = model.obj()
    print('\nObjective Value:', objective_value)

    print('######### SOLUCIÓN DEL MODELO #########\n')
    print('------------------------------------')
else:
    print("No se encontró una solución óptima.")


