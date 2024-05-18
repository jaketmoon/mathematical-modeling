from pyomo.environ import *
from pyomo.opt import SolverFactory
import numpy as np
# 定义咖啡种类及其属性
coffee = ["生椰拿铁", "香草拿铁", "酱香拿铁", "生酪拿铁", "丝绒拿铁", "厚乳拿铁", "标准美式", "加浓美式", "热红酒美式", "橙C美式", "卡布奇诺", "摩卡", "焦糖玛奇朵"]
price = [18, 17, 19, 18, 19, 19, 13, 16, 18, 18, 17, 17, 17]
cost = [10, 9, 12, 9, 11, 11, 6, 8, 9, 9, 8, 9, 9]
time = [3.5, 3.2, 4.5, 3.3, 3.4, 3.6, 2, 2.5, 2.7, 2.9, 4, 4, 4]
rating = [0.94, 0.9, 0.93, 0.92, 0.9, 0.95, 0.88, 0.86, 0.86, 0.87, 0.91, 0.9, 0.86]

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