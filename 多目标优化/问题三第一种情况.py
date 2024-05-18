from pyomo.environ import *
from pyomo.opt import SolverFactory
import numpy as np
price= [44,41,47,47,44,44,40,35,45,47,39,40,53,53,54,42,38,48,45,49]
cost=[38,45,41,49,40,39,46,40,49,40,43,43,47,48,50,45,42,44,51,40]
N = len(price)
Acost=41
Bcost=35
profit=np.subtract(price,cost)
I = range(1, N+1)
total_cost=0
all=0
target=0

m = ConcreteModel()


m.x = Var(I, domain=Binary)


for i in range(N):
    total_cost+=cost[i]*m.x[i+1]
    target+=profit[i]*m.x[i+1]
    all+=m.x[i+1]

m.con1 = Constraint(expr=target >=Acost)


m.obj = Objective(expr= all, sense = maximize)


# 创建求解器
opt = SolverFactory('glpk')


# 解决模型
instance = m.create_instance()
results = opt.solve(instance)



# 打印出结果
print("参与新品活动的门店有：")
for i in I:
    if(value(instance.x[i]==1)):
        print("门店", i)
    


print('---------------------------')
print( f'总店数为 {value(instance.obj)}' )
print('---------------------------')