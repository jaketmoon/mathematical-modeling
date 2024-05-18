import numpy as np
from scipy.optimize import linprog

# Given data
coffee_names = ["生椰拿铁", "香草拿铁", "酱香拿铁", "生酪拿铁", "丝绒拿铁", "厚乳拿铁", "标准美式", "加浓美式", 
                "热红酒美式", "橙C美式", "卡布奇诺", "摩卡", "焦糖玛奇朵"]
price = np.array([18, 17, 19, 18, 19, 19, 13, 16, 18, 18, 17, 17, 17])
cost = np.array([10, 9, 12, 9, 11, 11, 6, 8, 9, 9, 8, 9, 9])
rating = np.array([0.94, 0.9, 0.93, 0.92, 0.9, 0.95, 0.88, 0.86, 0.86, 0.87, 0.91, 0.9, 0.86])
time = np.array([3.5, 3.2, 4.5, 3.3, 3.4, 3.6, 2, 2.5, 2.7, 2.9, 4, 4, 4])

# Constants
daily_cost_limit = 10000  # Total daily cost budget
business_hours = 8        # Total daily business hours
min_avg_rating = 0.9      # Minimum average customer rating

# Calculating profit per coffee type
profit = price - cost

# Objective function: Maximize total profit
obj = -profit  # Negative sign because linprog does minimization

# Bounds for each variable (number of each coffee type sold)
bounds = [(0, None) for _ in range(len(coffee_names))]

# Constraints
# 1. Time constraint: Total time should not exceed business_hours*60 (convert hours to minutes)
time_constraint = time

# 2. Cost constraint: Total cost should not exceed daily_cost_limit
cost_constraint = cost

# Adding an auxiliary variable for total number of coffees sold
new_obj = np.append(obj, 0)  # No profit contribution from the auxiliary variable
new_bounds = bounds + [(0, None)]  # Bounds for the auxiliary variable

# Adjusting constraints to include the auxiliary variable
time_constraint = np.append(time_constraint, -60)  # Convert total coffees to time
cost_constraint = np.append(cost_constraint, 0)    # Cost constraint does not change

# New rating constraint
rating_constraint = np.append(rating - min_avg_rating, -1)

# Solve with all constraints
res = linprog(new_obj, A_ub=[time_constraint, cost_constraint], b_ub=[business_hours*60, daily_cost_limit],
              A_eq=[rating_constraint], b_eq=[0], bounds=new_bounds, method='highs')

# Final solution (excluding the auxiliary variable)
solution = res.x[:-1] if res.success else None
print(res)