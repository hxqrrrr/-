import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree

# 创建一个加权邻接矩阵
adj_matrix = np.array([[0, 6, 1, 5],
                       [6, 0, 5, 3],
                       [1, 5, 0, 6],
                       [5, 3, 6, 0]])

# 将邻接矩阵转换为稀疏矩阵
adj_sparse = csr_matrix(adj_matrix)

# 计算最小生成树
mst = minimum_spanning_tree(adj_sparse)

# 输出最小生成树的邻接矩阵
print(mst.toarray().astype(int))
