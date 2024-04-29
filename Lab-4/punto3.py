#Pyomo Imports (Modelo Matematico)
from pyomo.environ import *
from pyomo.opt import SolverFactory
# Respuesta: 5



# Sets
model = ConcreteModel()
model.i = Set(initialize=['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12', 'b13', 'b14', 'b15', 'b16', 'b17', 'b18', 'b19', 'b20'])
model.j = Set(initialize=['t1', 't2', 't3', 't4', 't5', 't6', 't7'])

# Parameters
def a_init(model, i, j):
    adyacencias = {
        ("b1", "t1"): 1, 
        ("b5", "t1"): 1,
        ("b2", "t2"): 1, 
        ("b3", "t2"): 1, 
        ("b6", "t2"): 1, 
        ("b7", "t2"): 1,
        ("b5", "t3"): 1, 
        ("b9", "t3"): 1,
        ("b8", "t4"): 1, 
        ("b12", "t4"): 1, 
        ("b16", "t4"): 1, 
        ("b19", "t4"): 1, 
        ("b20", "t4"): 1,
        ("b9", "t5"): 1, 
        ("b10", "t5"): 1, 
        ("b13", "t5"): 1, 
        ("b14", "t5"): 1,
        ("b10", "t6"): 1, 
        ("b11", "t6"): 1, 
        ("b14", "t6"): 1, 
        ("b15", "t6"): 1,
        ("b13", "t7"): 1, 
        ("b17", "t7"): 1
    }
    return adyacencias.get((i, j), 0)
#Crear la matriz
model.a = Param(model.i, model.j, initialize=a_init)

# Variables
model.s = Var(model.i, domain=Binary)   # Indica si se voltea la baldosa i

# Funcion objetivo
def objective_function(model):
    return sum(model.s[i] for i in model.i)
model.z = Objective(rule=objective_function, sense=minimize)

# Restricciones

def res1_rule(model, j):
    return sum(model.s[i] * model.a[i, j] for i in model.i) >= 1
model.res1 = Constraint(model.j, rule=res1_rule)


# Solver
SolverFactory('glpk').solve(model)
model.display()


# Mostrar resultados
print("Funcion objetivo (z):", model.z())
print("Baldosas giradas:")
for i in model.i:
    print("s[{}] = {}".format(i, model.s[i]()))

