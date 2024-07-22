import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 1. 数据准备
# 创建一个模拟的房价数据集
np.random.seed(42)
n_samples = 1000

area = np.random.uniform(50, 250, n_samples)
bedrooms = np.random.randint(1, 6, n_samples)
location_score = np.random.uniform(1, 10, n_samples)

# 模拟房价（加入一些非线性关系和噪声）
price = (area * 100 + bedrooms * 5000 + location_score * 10000
         + np.sin(area) * 1000 + np.random.normal(0, 10000, n_samples))

# 创建DataFrame
data = pd.DataFrame({
    'area': area,
    'bedrooms': bedrooms,
    'location_score': location_score,
    'price': price
})

# 2. 数据预处理
X = data[['area', 'bedrooms', 'location_score']]
y = data['price']

# 分割数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 标准化特征
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 3. 创建和训练BP神经网络
model = MLPRegressor(hidden_layer_sizes=(100, 50),
                     activation='relu',
                     solver='adam',
                     max_iter=1000,
                     random_state=42)

model.fit(X_train_scaled, y_train)

# 4. 评估模型
y_pred = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"均方误差 (MSE): {mse:.2f}")
print(f"决定系数 (R^2): {r2:.2f}")

# 5. 可视化结果
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel("实际价格")
plt.ylabel("预测价格")
plt.title("房价预测：实际 vs 预测")
plt.tight_layout()
plt.show()

# 6. 使用模型进行预测
new_house = np.array([[150, 3, 7]])  # 面积150平方米，3间卧室，地段评分7
new_house_scaled = scaler.transform(new_house)
predicted_price = model.predict(new_house_scaled)

print(f"新房屋预测价格: {predicted_price[0]:.2f}")
