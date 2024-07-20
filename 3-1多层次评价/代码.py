import numpy as np
from scipy.linalg import eig

# 构建判断矩阵
def create_judgment_matrix(n):
    matrix = np.ones((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i, j] = float(input(f"请输入元素 {i+1} 相对于元素 {j+1} 的重要性："))
            matrix[j, i] = 1 / matrix[i, j]
    return matrix

# 计算特征向量和特征值
def compute_eigen(matrix):
    eigvals, eigvecs = eig(matrix)
    max_eigval = np.max(eigvals).real
    eigvec = eigvecs[:, np.argmax(eigvals)].real
    eigvec = eigvec / np.sum(eigvec)  # 归一化
    return max_eigval, eigvec

# 一致性检验
def consistency_check(matrix, max_eigval):
    n = matrix.shape[0]
    CI = (max_eigval - n) / (n - 1)
    RI = [0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45]  # 随机一致性指标
    CR = CI / RI[n - 1]
    return CR2

# 主程序
if __name__ == "__main__":
    n = int(input("请输入判断矩阵的维度："))
    judgment_matrix = create_judgment_matrix(n)
    print("判断矩阵：")
    print(judgment_matrix)

    max_eigval, eigvec = compute_eigen(judgment_matrix)
    print("最大特征值：", max_eigval)
    print("特征向量（权重）：", eigvec)

    CR = consistency_check(judgment_matrix, max_eigval)
    print("一致性比例（CR）：", CR)

    if CR < 0.1:
        print("判断矩阵的一致性通过。")
    else:
        print("判断矩阵的一致性未通过，请重新调整判断矩阵。")
