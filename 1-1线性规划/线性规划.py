from scipy.optimize import linprog
import numpy as np

# 定义问题中的参数
M = 10000  # 总投资金额
revenue = [0.10, 0.28, 0.21, 0.23, 0.25]  # 收益率，包括一个低收益的无风险投资
risk = [0, 0.025, 0.015, 0.055, 0.026]  # 风险损失率，包括无风险投资
trans_fee = [0, 0.01, 0.02, 0.045, 0.065]  # 交易费率，包括无交易费投资
min_amount = [0, 103, 198, 52, 40]  # 最低每份购买金额，包括无最低金额的投资

# 定义目标函数的系数（注意这里要取负，因为 linprog 默认是最小化问题）
c = [-revenue_i for revenue_i in revenue]
a = 0.01

# 定义等式约束矩阵和向量
A_eq = [
    [1 + trans_fee[0], 1 + trans_fee[1], 1 + trans_fee[2], 1 + trans_fee[3], 1 + trans_fee[4]],
]
b_eq = [M]

# 定义不等式约束矩阵和向量
A_ub = [risk]  # 风险约束
b_ub = [a * M]  # 风险上限

# 定义变量的上下界
x_bounds = [(min_amount[i], None) for i in range(5)]

# 求解线性规划问题
result = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=x_bounds, method='highs')

# 输出结果
if result.success:
    print("最优解：")
    print("投资金额：", M)
    print("每份购买金额：", np.round(result.x, 2))
    total_revenue = np.dot(result.x, revenue)  # 计算总收益
    total_risk = np.dot(result.x, risk) 
    print("收益：", np.round(total_revenue, 2))
    print("风险：", np.round(total_risk/M, 2))
else:
    print("无可行解！")
