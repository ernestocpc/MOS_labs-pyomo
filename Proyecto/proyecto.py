# -*- coding: utf-8 -*-
"""
Quiz 5 - Proyecto
Autores: Maria Alejandra Estrada - 202021060
         Ernesto Carlos Perez - 202112530
"""

#Importaciones
from pyomo.environ import *
from pyomo.opt import SolverFactory

import sys
import os


#Creación modelo
model = ConcreteModel()

# Conjuntos
model.i = Set(initialize=['p1', 'p2', 'p3'])
model.j = Set(initialize=model.i)
model.k = Set(initialize=['d', 'e', 'a'])

# Parametros
model.D = Param(initialize=2)
model.E = Param(initialize=1)
model.A = Param(initialize=4)

prioridades={
    ('p1', 'p1'): 5, ('p1', 'p2'): 2, ('p1', 'p3'): 0,
    ('p2', 'p1'): 3, ('p2', 'p2'): 2, ('p2', 'p3'): 0,
    ('p3', 'p1'): 3, ('p3', 'p2'): 5, ('p3', 'p3'): 0
}
model.P = Param(model.i, model.j, initialize=prioridades)

doctores={
    ('p1', 'p1'): 2, ('p1', 'p2'): 0, ('p1', 'p3'): 0,
    ('p2', 'p1'): 0, ('p2', 'p2'): 0, ('p2', 'p3'): 0,
    ('p3', 'p1'): 1, ('p3', 'p2'): 0, ('p3', 'p3'): 0
} 
model.numD = Param(model.i, model.j, initialize=doctores)

enfemeras={
    ('p1', 'p1'): 0, ('p1', 'p2'): 2, ('p1', 'p3'): 1,
    ('p2', 'p1'): 2, ('p2', 'p2'): 2, ('p2', 'p3'): 1,
    ('p3', 'p1'): 0, ('p3', 'p2'): 0, ('p3', 'p3'): 0
}
model.numE = Param(model.i, model.j, initialize=enfemeras)

administradores={
    ('p1', 'p1'): 0, ('p1', 'p2'): 0, ('p1', 'p3'): 0,
    ('p2', 'p1'): 0, ('p2', 'p2'): 0, ('p2', 'p3'): 0,
    ('p3', 'p1'): 0, ('p3', 'p2'): 1, ('p3', 'p3'): 1
}
model.numA = Param(model.i, model.j, initialize=administradores) 

# Variables de decisión
model.X = Var(model.i, model.j, domain=Binary)  
model.Y = Var(model.i, model.j, model.k, domain=NonNegativeIntegers) 

# Solver
SolverFactory('glpk').solve(model)
model.display()
print('######### SOLUCIÓN DEL MODELO #########\n')
print('------------------------------------')