import numpy as np
from scipy.optimize import minimize

# 定义目标函数
def objective(x, dp, dm, i):
    if i == 0:
        return dp[0] 
    elif i == 1:
        return dm[1] + dp[1]
    elif i == 2:
        return dm[2]
    else:
        return 0  # 确保在所有情况下都有返回值

# 定义约束条件
def constraint1(x):
    return 11 - (2 * x[0] + x[1])

def constraint2(x, dp, dm):
    return x[0] - x[1] + dp[0] - dm[0]

def constraint3(x, dp, dm):
    return x[0] + 2 * x[1] + dp[1] - dm[1] - 10

def constraint4(x, dp, dm):
    return 8 * x[0] + 10 * x[1] + dp[2] - dm[2] - 56

# 初始化变量
x0 = [3, 5]
dp0 = [2, 0, 0]
dm0 = [0, 3, 18]

# 设置约束
constraints = [{'type': 'ineq', 'fun': constraint1},
               {'type': 'eq', 'fun': lambda x: constraint2(x, dp0, dm0)},
               {'type': 'eq', 'fun': lambda x: constraint3(x, dp0, dm0)},
               {'type': 'eq', 'fun': lambda x: constraint4(x, dp0, dm0)}]          

# 设置边界
bounds = [(0, None), (0, None)]

# 优化过程
goal = np.ones(3) * 100000
for i in range(3):
    res = minimize(lambda x: objective(x, dp0, dm0, i), x0, bounds=bounds, constraints=constraints)
    print(f'第{i+1}级目标求解为：')
    print(f'目标函数值: {res.fun}')
    print(f'x: {res.x}')
    print(f'dm: {dm0}')
    print(f'dp: {dp0}')
    goal[i] = res.fun
    # 更新约束条件
    obj_val = objective(x0, dp0, dm0, i+1)
    if obj_val is not None:
        constraints.append({'type': 'ineq', 'fun': lambda x: obj_val - goal[i]})
    print(res.fun)
