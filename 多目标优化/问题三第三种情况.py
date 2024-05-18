from pyomo.environ import *
from pyomo.opt import SolverFactory
import numpy as np

# 定义价格、成本
price = [44, 41, 47, 47, 44, 44, 40, 35, 45, 47, 39, 40, 53, 53, 54, 42, 38, 48, 45, 49, 40, 34, 53, 47, 54, 43, 43, 40, 43, 40, 45, 47, 49, 41, 42, 50, 40, 49, 44, 46]
cost = [38, 45, 41, 49, 40, 39, 46, 40, 49, 40, 43, 43, 47, 48, 50, 45, 42, 44, 51, 40, 35, 40, 50, 52, 51, 49, 48, 36, 37, 38, 41, 42, 43, 47, 46, 45, 39, 44, 49, 41]
N = len(price)
Acost = 41#运营商1的成本
Bcost = 35#运营商2的成本
profit = np.subtract(price, cost)#每个店的利润
I = range(1, N+1)

#定义总成本，总数量和总利润
total_cost = 0
all = 0
target = 0#总利润

# 创建一个具体模型
m = ConcreteModel()

# 定义决策变量
m.x = Var(I, domain=Binary)

# 设置约束条件和目标函数
for i in range(N):
    total_cost += cost[i] * m.x[i+1]
    target += profit[i] * m.x[i+1]
    all += m.x[i+1]

m.con1 = Constraint(expr=target >= Acost + Bcost)
m.obj = Objective(expr=all, sense=maximize)

# 创建求解器
opt = SolverFactory('glpk')

# 解决模型
instance = m.create_instance()
results = opt.solve(instance)

# 打印结果
print("参与新品活动的门店有：")
for i in I:
    if value(instance.x[i]) == 1:
        print("门店", i)

print('---------------------------')
print(f'总店数为 {value(instance.obj)}')
print('---------------------------')