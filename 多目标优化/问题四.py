from pyomo.environ import *
from pyomo.opt import SolverFactory
import numpy as np
import math


# 定义价格、成本
price = [44, 41, 47, 47, 44, 44, 40, 35, 45, 47, 39, 40, 53, 53, 54, 42, 38, 48, 45, 49, 40, 34, 53, 47, 54, 43, 43, 40, 43, 40, 45, 47, 49, 41, 42, 50, 40, 49, 44, 46]
cost = [38, 45, 41, 49, 40, 39, 46, 40, 49, 40, 43, 43, 47, 48, 50, 45, 42, 44, 51, 40, 35, 40, 50, 52, 51, 49, 48, 36, 37, 38, 41, 42, 43, 47, 46, 45, 39, 44, 49, 41]
shop=np.ones(40)
N = len(price)
Acost = 41#运营商1的成本
Bcost = 35#运营商2的成本
profit = np.subtract(price, cost)#每个店的利润
I = range(1, N+1)
J=range(1, 3)
## -------------------------------- ##

np.set_printoptions(precision = 2)


## -------------------------------- ##L2归一化
def _norm_matrix( mat ):

    mat_tmp = mat
    _norm=0
    _N = len( mat)
    for i in range( _N ):
        _norm+=mat[i]**2
    _norm=math.sqrt(2)
    for j in range( _N ):
        mat_tmp[j]  = mat[j] / _norm

    return mat_tmp
## -------------------------------- ##

mat_cost= _norm_matrix(cost)
mat_shop=_norm_matrix(shop)

## -------------------------------- ##


total_cost=0
all_new=0
total_costnew=0

m = ConcreteModel()

m.x = Var(I, domain=Binary)


for i in range(N):
    total_cost=cost[i]*m.x[i+1]#成本
    all_new+=m.x[i+1]*mat_shop[i]
    total_costnew+=m.x[i+1]*mat_cost[i]



m.con01 = Constraint(expr=total_cost<= 1200-Acost-Bcost)

m.obj = Objective(expr= (total_costnew*0.65+all_new*0.35) , sense = maximize)


opt = SolverFactory('glpk')

opt.solve(m, tee=True)
for i in I:
    if value(m.x[i]) == 1:
        print("门店", i)

print('---------------------------')
print( f'The objective is {value(m.obj)}' )
print('---------------------------')