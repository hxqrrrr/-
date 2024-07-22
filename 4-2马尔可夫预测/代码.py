import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


# 定义状态转移矩阵
transition_matrix = np.array([
    [0.7, 0.2, 0.1],
    [0.3, 0.5, 0.2],
    [0.2, 0.3, 0.5]
])

# 定义初始状态
initial_state = np.array([1, 0, 0])

# 预测步数
steps = 20

# 进行预测
predictions = [initial_state]
for _ in range(steps):
    next_state = np.dot(predictions[-1], transition_matrix)
    predictions.append(next_state)

# 转换为numpy数组以便于绘图
predictions = np.array(predictions)

# 绘制结果
plt.figure(figsize=(10, 6))
plt.plot(predictions[:, 0], label='状态 1')
plt.plot(predictions[:, 1], label='状态 2')
plt.plot(predictions[:, 2], label='状态 3')
plt.xlabel('步数')
plt.ylabel('概率')
plt.title('马尔可夫链预测')
plt.legend()
plt.grid(True)
plt.show()
