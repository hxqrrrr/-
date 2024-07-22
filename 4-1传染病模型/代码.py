import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def sir_model(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# 设置参数
N = 10000  # 总人口
I0, R0 = 100, 0  # 初始感染者和康复者数量
S0 = N - I0 - R0  # 初始易感者数量
beta, gamma = 0.3, 0.1  # 传染率和恢复率
t = np.linspace(0, 100, 1000)  # 时间点

# 求解ODE
solution = odeint(sir_model, [S0, I0, R0], t, args=(N, beta, gamma))
S, I, R = solution.T

# 绘图
plt.figure(figsize=(10,6))
plt.plot(t, S, 'b', label='易感者(S)')
plt.plot(t, I, 'r', label='感染者(I)')
plt.plot(t, R, 'g', label='康复者(R)')
plt.xlabel('时间')
plt.ylabel('人数')
plt.title('SIR模型')
plt.legend()
plt.show()
