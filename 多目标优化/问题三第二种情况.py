from pyomo.environ import *
from pyomo.opt import SolverFactory
import numpy as np
price= [40,34,53,47,54,43,43,40,43,40,45,47,49,41,42,50,40,49,44,46]
cost=[35,40,50,52,51,49,48,36,37,38,41,42,43,47,46,45,39,44,49,41]
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

m.con1 = Constraint(expr=target >=Bcost)


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
        print("门店", 20+i)
    


print('---------------------------')
print( f'总店数为 {value(instance.obj)}' )
print('---------------------------')