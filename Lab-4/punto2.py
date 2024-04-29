#Plot Imports
import matplotlib.pyplot as plt

#Pyomo Imports (Modelo Matematico)
from pyomo.environ import *
from pyomo.opt import SolverFactory


# Sets
numNodes = 6
model = ConcreteModel()
model.p = Set(initialize=['p1', 'p2', 'p3', 'p4', 'p5', 'p6'])
model.j = Set(initialize=model.p)
N=RangeSet(1,numNodes)
cost = {
    ('p1', 'p1'): 0, ('p1', 'p2'): 10, ('p1', 'p3'): 20, ('p1', 'p4'): 30, ('p1', 'p5'): 30, ('p1', 'p6'): 20,
    ('p2', 'p1'): 10, ('p2', 'p2'): 0, ('p2', 'p3'): 25, ('p2', 'p4'): 35, ('p2', 'p5'): 20, ('p2', 'p6'): 10,
    ('p3', 'p1'): 20, ('p3', 'p2'): 25, ('p3', 'p3'): 0, ('p3', 'p4'): 15, ('p3', 'p5'): 30, ('p3', 'p6'): 20,
    ('p4', 'p1'): 30, ('p4', 'p2'): 35, ('p4', 'p3'): 15, ('p4', 'p4'): 0, ('p4', 'p5'): 15, ('p4', 'p6'): 25,
    ('p5', 'p1'): 30, ('p5', 'p2'): 20, ('p5', 'p3'): 30, ('p5', 'p4'): 15, ('p5', 'p5'): 0, ('p5', 'p6'): 14,
    ('p6', 'p1'): 20, ('p6', 'p2'): 10, ('p6', 'p3'): 20, ('p6', 'p4'): 25, ('p6', 'p5'): 14, ('p6', 'p6'): 0
}

# Variables
model.x = Var(model.p, domain=Binary)   # Indica si se elige el pueblo p

# Funcion objetivo
def objective_function(model):
    return sum(model.x[i] for i in model.x)
model.z = Objective(rule=objective_function, sense=minimize)

# Restricciones
def queEsteCerca_rule(model, i):
    return sum(model.x[j] for j in model.j if cost[i, j] <= 15) >= 1
model.queEsteCerca = Constraint(model.p, rule=queEsteCerca_rule) 


# Solver
SolverFactory('glpk').solve(model)
#model.display()

# Mostrar resultados
print("Funcion objetivo (z):", model.z())
print("Pueblos seleccionados:")
for i in model.j:
    print("s[{}] = {}".format(i, model.x[i]()))