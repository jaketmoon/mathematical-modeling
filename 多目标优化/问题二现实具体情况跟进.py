from pyomo.environ import *
from pyomo.opt import SolverFactory
import numpy as np
# 定义咖啡种类及其属性
coffee = [ "酱香拿铁",   "焦糖玛奇朵"]
price = [  19,  17]
cost = [  12, 9]
time = [  4.5,  4]
rating = [  0.93, 0.86]

# 初始化变量以存储总成本、总时间、平均评分、咖啡总数和目标值
total_cost = 0
N = len(coffee)
profit=np.subtract(price,cost)
I = range(1, N+1)
total_cost=0
total_time=0
average_rating=0
all=0
target=0


# 创建了一个具体模型
m = ConcreteModel()

# 定义决策变量
m.x = Var(I, domain=NonNegativeIntegers)

# 定义变量以存储总成本、总时间、平均评分、咖啡总数和目标值
for i in range(N):
    total_cost+=cost[i]*m.x[i+1]
    total_time+=time[i]*m.x[i+1]
    target+=profit[i]*m.x[i+1]
    average_rating+=rating[i]*m.x[i+1]
    all+=m.x[i+1]


# 定义约束条件
m.con1 = Constraint(expr= total_cost <= 10000 )

m.con2 = Constraint(expr=total_time <= 480 )

m.con3 = Constraint(expr=average_rating >= 0.9*all )

# 定义目标函数
m.obj = Objective(expr= target, sense = maximize)


# 创建求解器
opt = SolverFactory('glpk')


# 解决模型
instance = m.create_instance()
results = opt.solve(instance)



# 打印出结果
for i in I:
    print("购买", coffee[i-1], ":", value(instance.x[i]))

print('---------------------------')
print( f'最大获利为 {value(instance.obj)}' )
print('---------------------------')