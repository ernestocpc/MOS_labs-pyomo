# -*- coding: utf-8 -*-
"""
Lab 6 - Punto 1
Autores: Maria Alejandra Estrada - 202021060
         Ernesto Carlos Perez - 202112530
"""

#Plot Imports
import matplotlib.pyplot as plt

#Pyomo Imports
from pyomo.environ import *
from pyomo.opt import SolverFactory

#Creación Modelo
Model = ConcreteModel()

# Sets
Model.N = RangeSet(1, 5)

"""
Agregamos entonces como restricción la función de hops: Fhops(x) ≤ epsilon. El epsilon debería tener 
un valor que permitiera que la función de hops sea factible según el escenario que estemos resolviendo. 
Por ejemplo, un valor de epsilon podría ser 5, o sea Fhops(x) ≤ 5. Si resolvemos el modelo con este valor 
de epsilon, la ruta de 1 a 5  sería la 1-3-4-5 y los valores de la funciones serían 15 para la función de costo 
y 3 para la de hops, obteniendo así un primer punto del frente de Pareto. Si empezamos a decrementar de a 1 el 
valor de epsilon, veremos que con epsilon=2 la ruta de 1 a 5 sería 1-2-5, generando los valores de 20 para la 
función de costo y 2 para la función de hops, obteniendo así un segundo punto del frente de Pareto. Si el epsilon 
es igual a 1, obtendríamos infactibilidad ya que no es posible encontrar una solución en la cual el número de hops 
sea 1 o menor a 1. De esta manera, la idea sería poner a cambiar el epsilon hasta donde sepamos que el modelo va a ser factible.
"""

# Hops
Model.h = Param(Model.N, Model.N, mutable=True)

for i in Model.N:
    for j in Model.N:
        Model.h[i, j] = 999

Model.h[1, 2] = 1
Model.h[1, 3] = 1
Model.h[2, 5] = 1
Model.h[3, 4] = 1
Model.h[4, 5] = 1

# Costos
Model.c = Param(Model.N, Model.N, mutable=True)

for i in Model.N:
    for j in Model.N:
        Model.c[i, j] = 999

Model.c[1, 2] = 10
Model.c[1, 3] = 5
Model.c[2, 5] = 10
Model.c[3, 4] = 5
Model.c[4, 5] = 5

# Origen y destino
o = 1
d = 5

# Variables de decisión
Model.x = Var(Model.N, Model.N, domain=Binary)

# Posibles funciones objetivos
Model.f1 = sum(Model.x[i, j] * Model.h[i, j] for i in Model.N for j in Model.N) #Función de hops
Model.f2 = sum(Model.x[i, j] * Model.c[i, j] for i in Model.N for j in Model.N) #Función de costos

# Restricción 1
def res1(Model, i):
    if i == o:
        return sum(Model.x[i, j] for j in Model.N) == 1
    else:
        return Constraint.Skip

Model.res1 = Constraint(Model.N, rule=res1)

# Restricción 2
def res2(Model, j):
    if j == d:
        return sum(Model.x[i, j] for i in Model.N) == 1
    else:
        return Constraint.Skip

Model.res2 = Constraint(Model.N, rule=res2)

# Restricción 3
def res3(Model, i):
    if i != o and i != d:
        return sum(Model.x[i, j] for j in Model.N) - sum(Model.x[j, i] for j in Model.N) == 0
    else:
        return Constraint.Skip

Model.res3 = Constraint(Model.N, rule=res3)

# Función objetivo
"""
Deseamos minimizar dos funciones, función de costo y función de hops. Con e-Constraint solo podemos 
dejar una única función como función objetivo general. Por ejemplo, podríamos dejar a la función de 
costo como función general.
"""
Model.obj = Objective(expr=Model.f2, sense=minimize)

# Epsilon
epsilon_values = [5, 4, 3, 2, 1]

# Frente de pareto
f1_values = []
f2_values = []

# Solver para los diferentes epsilons
for epsilon in epsilon_values:
    # Restricción de Hops f1
    def hops_res(Model):
        return Model.f1 <= epsilon

    Model.hops_res = Constraint(rule=hops_res)

    SolverFactory('glpk').solve(Model)

    f1_values.append(value(Model.f1))
    f2_values.append(value(Model.f2))

    Model.del_component(Model.hops_res)

# Plot d3 multiobjetivoHopsCosts_sumasPonderadas.py
plt.plot(f1_values,f2_values,'o-.');
plt.title('Frente Óptimo de Pareto');
plt.xlabel('F1')
plt.ylabel('F2')

plt.grid(True);
plt.show()

