from scipy.optimize import linprog
import numpy as np

# 定义距离函数
def fun(x1,x2,y1,y2):
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)
    
#x_labels = 6个工地，y_labels = 2个工厂
Consumption_Location = [[1.25,8.75,0.5,5.75,3,7.25],
                        [1.25,0.75,4.75,5,6.5,7.75]]
#工地日消耗量
Comsumption_Daily = [3,5,4,7,6,11]   
#距离矩阵，x_label是6个工地，y_label是2个工厂           
Distance_Matrix = [[fun(5, Consumption_Location[0][i], 1, Consumption_Location[1][i]) for i in range(6) ],
                   [fun(2, Consumption_Location[0][i], 7, Consumption_Location[1][i]) for i in range(6) ]]

#目标函数
target = [fun(5, Consumption_Location[0][i], 1, Consumption_Location[1][i]) for i in range(6)
            ] + [fun(2, Consumption_Location[0][i], 7, Consumption_Location[1][i]) for i in range(6) ]


# 定义等式约束矩阵和向量
A_eq = [
    [1,0,0,0,0,0,1,0,0,0,0,0],
    [0,1,0,0,0,0,0,1,0,0,0,0],
    [0,0,1,0,0,0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0,0,0,1,0,0],
    [0,0,0,0,1,0,0,0,0,0,1,0],
    [0,0,0,0,0,1,0,0,0,0,0,1]
]

b_eq = Comsumption_Daily

# 定义不等式约束矩阵和向量
A_ub = [[1,1,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,1,1,1,1,1]]  # 风险约束
b_ub = [20,20]  # 风险上限

# 定义变量的上下界
x_bounds = [(0,11) for i in range(12)]

# 求解线性规划问题
result = linprog(target, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=x_bounds, method='highs')

# 输出结果
print(result)
