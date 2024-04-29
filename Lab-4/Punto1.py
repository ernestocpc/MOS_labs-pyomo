# -*- coding: utf-8 -*-
"""
Laboratorio 4 - Punto 1

Maria Alejandra Estrada - 202021060
Ernesto Carlos Perez - 202112530
"""

from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

import sys
import os

os.system("clear")

Model = ConcreteModel()

# SETS & PARAMETERS********************************************************************

numOrigenes = 3
numDestinos = 2
numTipo = 2

Model.Origin = RangeSet(1, numOrigenes)
Model.Dest =  RangeSet(1, numDestinos)
Model.Tipo = RangeSet(1, numTipo)

#Costo de enviar un proceso de origen a destino
Model.cost = Param(Model.Origin, Model.Dest, mutable=True)

Model.cost[1,1] = 300
Model.cost[1,2] = 500
Model.cost[2,1] = 200
Model.cost[2,2] = 300
Model.cost[3,1] = 600
Model.cost[3,2] = 300

#Oferta por origen y tipo
Model.oferta = Param(Model.Origin, Model.Tipo, mutable=True)

Model.oferta[1,1] = 60
Model.oferta[2,1] = 80
Model.oferta[3,1] = 50
Model.oferta[1,2] = 80
Model.oferta[2,2] = 50
Model.oferta[3,2] = 50

#Demanda por destino y tipo
Model.demanda = Param(Model.Dest, Model.Tipo, mutable=True)

Model.demanda[1,1] = 100
Model.demanda[2,1] = 90
Model.demanda[1,2] = 60
Model.demanda[2,2] = 120


# VARIABLES****************************************************************************

#Cantidad de procesos de origen x a destino y con tipo
Model.x = Var(Model.Origin, Model.Dest, Model.Tipo, domain=PositiveReals)

# OBJECTIVE FUNCTION*******************************************************************

#Costo total de todas las transferencias
Model.obj = Objective(expr = sum(Model.cost[i,j]*Model.x[i,j,k] for i in Model.Origin for j in Model.Dest for k in Model.Tipo))


# CONSTRAINTS**************************************************************************

#Dado por origen
Model.res1 = ConstraintList()
for i in Model.Origin:
    for k in Model.Tipo:
        Model.res1.add(sum(Model.x[i,j,k] for j in Model.Dest) == Model.oferta[i,k])

#Recibido por destino
Model.res2 = ConstraintList()
for j in Model.Dest:
    for k in Model.Tipo:
        Model.res2.add(sum(Model.x[i,j,k] for i in Model.Origin) == Model.demanda[j,k])


# APPLYING THE SOLVER******************************************************************
SolverFactory('glpk').solve(Model)

Model.display()