import numpy as np
import pandas as pd

# 输入数据
data = pd.DataFrame({
    '学生编号': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    '语文': [93, 97, 65, 97, 85, 63, 71, 82, 99, 99],
    '数学': [66, 99, 99, 79, 92, 65, 77, 97, 92, 98],
    '物理': [86, 61, 94, 61, 67, 91, 78, 86, 89, 66],
    '化学': [88, 61, 71, 92, 96, 93, 88, 73, 83, 80],
    '英语': [77, 75, 91, 66, 80, 80, 78, 86, 66, 82],
    '政治': [71, 87, 86, 66, 64, 80, 99, 73, 85, 69],
    '生物': [90, 70, 80, 88, 96, 99, 78, 73, 83, 70],
    '历史': [94, 70, 93, 69, 98, 74, 99, 70, 85, 79]
})

# 熵权法函数
def entropy_weight(data):
    # 标准化
    norm_data = data.iloc[:, 1:] / data.iloc[:, 1:].sum(axis=0)

    # 计算熵值
    k = 1 / np.log(len(data))
    entropy = -k * (norm_data * np.log(norm_data + 1e-10)).sum(axis=0)

    # 计算冗余度
    redundancy = 1 - entropy

    # 计算权重
    weights = redundancy / redundancy.sum()

    return weights

# 计算权重
weights = entropy_weight(data)
print("指标权重:", weights)

# 计算综合得分
scores = (data.iloc[:, 1:] * weights).sum(axis=1)
data['综合得分'] = scores

# 排序
sorted_data = data.sort_values(by='综合得分', ascending=False)
print("排序结果:\n", sorted_data[['学生编号', '综合得分']])
