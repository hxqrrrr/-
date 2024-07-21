import numpy as np


def GM11(x0):
    """
    GM(1,1) 灰色预测模型
    :param x0: 原始数据序列
    :return: 预测值，a和b参数
    """
    x1 = x0.cumsum()  # 累加生成序列
    n = len(x0)
    B = np.zeros((n - 1, 2))
    Y = x0[1:].reshape((n - 1, 1))
    for i in range(n - 1):
        B[i][0] = -0.5 * (x1[i] + x1[i + 1])
        B[i][1] = 1.0
    BT = B.T
    a_b = np.linalg.inv(BT @ B) @ BT @ Y
    a, b = a_b[0][0], a_b[1][0]

    def f(k):
        return (x0[0] - b / a) * np.exp(-a * k) + b / a

    x_hat = np.array([f(i) for i in range(n)])
    return x_hat, a, b


# 输入数据
data = np.array([71.1, 72.4, 72.4, 72.1, 71.4, 72.0, 71.6])

# 模型预测
x_hat, a, b = GM11(data)

# 打印结果
print("原始数据:", data)
print("预测数据:", x_hat)
print("a参数:", a)
print("b参数:", b)

# 可行性检验
residuals = data - x_hat  # 残差
relative_errors = residuals / data  # 相对误差

print("残差:", residuals)
print("相对误差:", relative_errors)

# 计算残差和相对误差的均值和标准差
residuals_mean = np.mean(residuals)
residuals_std = np.std(residuals)
relative_errors_mean = np.mean(relative_errors)
relative_errors_std = np.std(relative_errors)

print("残差均值:", residuals_mean)
print("残差标准差:", residuals_std)
print("相对误差均值:", relative_errors_mean)
print("相对误差标准差:", relative_errors_std)

# 级比检验
lambda_k = data[1:] / data[:-1]
lambda_lower = np.exp(-2 / (len(data) + 1))
lambda_upper = np.exp(2 / (len(data) + 1))

print("级比:", lambda_k)
print("理论级比区间: [{:.4f}, {:.4f}]".format(lambda_lower, lambda_upper))

# 判断级比是否在理论区间内
is_within_range = np.all((lambda_k >= lambda_lower) & (lambda_k <= lambda_upper))
print("级比是否在理论区间内:", is_within_range)

# 未来预测
future_point = len(data)  # 预测下一年的数据
future_x = (data[0] - b / a) * np.exp(-a * future_point) + b / a
print("1993年预测数据:", future_x)
