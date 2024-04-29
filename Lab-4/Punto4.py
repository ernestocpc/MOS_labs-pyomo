# -*- coding: utf-8 -*-
"""
Laboratorio 4 - Punto 4

Maria Alejandra Estrada - 202021060
Ernesto Carlos Perez - 202112530
"""


from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

import sys
import os

import numpy as np
import matplotlib.pyplot as plt

 
os.system("clear")

Model = ConcreteModel()

# SETS & PARAMETERS********************************************************************

numNodos = 7

Model.Nodos = RangeSet(1, numNodos)


#Cordenadas en X
Model.CordX = Param(Model.Nodos, mutable=True)

Model.CordX[1] = 20
Model.CordX[2] = 22
Model.CordX[3] = 9
Model.CordX[4] = 3
Model.CordX[5] = 21
Model.CordX[6] = 29
Model.CordX[7] = 14

#Cordenadas en Y
Model.CordY = Param(Model.Nodos, mutable=True)

Model.CordY[1] = 6
Model.CordY[2] = 1
Model.CordY[3] = 2
Model.CordY[4] = 25
Model.CordY[5] = 10
Model.CordY[6] = 2
Model.CordY[7] = 12

#Distancias entre nodos
Model.Dist = Param(Model.Nodos, Model.Nodos, mutable=True)

for i in Model.Nodos:
    for j in Model.Nodos:
        
        temp = sqrt((Model.CordX[i].value - Model.CordX[j].value)**2 + (Model.CordY[i].value - Model.CordY[j].value)**2)
        
        if i!=j and temp<=20:
            Model.Dist[i,j] = temp
        else:
            Model.Dist[i,j] = 999999
            

# VARIABLES****************************************************************************

#Si se toma un camino o no
Model.x = Var(Model.Nodos, Model.Nodos, domain=Binary)


# OBJECTIVE FUNCTION*******************************************************************

#Minimizar la distancia
Model.obj = Objective(expr = sum(Model.x[i,j]*Model.Dist[i,j] for i in Model.Nodos for j in Model.Nodos))


# CONSTRAINTS**************************************************************************

#Nodo origen
Model.res1 = ConstraintList()
 
for i in Model.Nodos:
    if i==4:
        Model.res1.add(sum(Model.x[i,j] for j in Model.Nodos) == 1)
        
#Nodo destino
Model.res2 = ConstraintList()

for j in Model.Nodos:
    if j==6:
        Model.res2.add(sum(Model.x[i,j] for i in Model.Nodos) == 1)

#Nodo intermedio
Model.res3 = ConstraintList()

for i in Model.Nodos:
    if i != 4 and i !=6:
        Model.res3.add((sum(Model.x[i,j] for j in Model.Nodos)-sum(Model.x[j,i] for j in Model.Nodos)) == 0 )


# APPLYING THE SOLVER******************************************************************
SolverFactory('glpk').solve(Model)

#Model.display()

# GRAFICAR****************************************************************************
resp = np.array([[Model.x[i, j].value for j in Model.Nodos] for i in Model.Nodos])
dist =  np.array([[Model.Dist[i, j].value for j in Model.Nodos] for i in Model.Nodos])
x = np.array([Model.CordX[i].value for i in Model.Nodos])
y = np.array([Model.CordY[i].value for i in Model.Nodos])
names = np.array(['N' + str(i) for i in Model.Nodos])

plt.style.use('ggplot')
plt.figure()
plt.plot(x,y, 'ko')#Puntos

#texto
for i,name in enumerate(names):
    plt.text(x[i]+0.5,y[i], name, size=8)

#Lineas
n = len(dist)
for i in range(n):
    for j in range(i, n):
        if dist[i,j] <= 20:
            
            if resp[i,j] == 0 and resp[j,i] == 0:
                plt.plot([x[i],x[j]],[y[i],y[j]],'k--')
            else:
                plt.plot([x[i],x[j]],[y[i],y[j]],'r-')
        
            
Model.display()    
plt.show()