"""
Quiz 5 - Proyecto
Autores: Maria Alejandra Estrada - 202021060
         Ernesto Carlos Perez - 202112530
"""

#Importaciones
from pyomo.environ import *
from pyomo.opt import SolverFactory

#Creación modelo
model = ConcreteModel()

# Conjuntos y parametros

model.Z = Set(initialize=['urgencias', 'consultorios', 'cirugias', 'hospitalarios'])
model.i = Set(initialize=model.Z)
model.j = Set(initialize=model.Z)
model.k = Set(initialize=['d', 'e', 'a'])
model.D = Set()
model.E = Set()
model.A = Set()

model.P = Param(model.i, model.j, initialize=0)  
model.numD = Param(model.i, model.j, initialize=0)  
model.numE = Param(model.i, model.j, initialize=0) 
model.numA = Param(model.i, model.j, initialize=0) 

# Variables de decisión
model.X = Var(model.i, model.j, domain=Binary)  
model.A = Var(model.i, model.j, model.k, domain=NonNegativeIntegers) 

#SolverFactory('mindtpy').solve(Model, mip_solver='glpk', nlp_solver='ipopt')
#Model.display()
print('######### SOLUCIÓN DEL MODELO #########\n')
print('------------------------------------')