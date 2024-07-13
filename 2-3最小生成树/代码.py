import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree, dijkstra

# 创建一个加权邻接矩阵
adj_matrix = np.array([[0 , 2 , 1 , 3 , 4 , 4 , 2 , 5 , 4 ],
                       [2 , 0 , 4 , 0 , 0 , 0 , 0 , 0 , 1 ],
                       [1 , 4 , 0 , 1 , 0 , 0 , 0 , 0 , 0 ],
                       [3 , 0 , 1 , 0 , 1 , 0 , 0 , 0 , 0 ],
                       [4 , 0 , 0 , 1 , 0 , 5 , 0 , 0 , 0 ],
                       [4 , 0 , 0 , 0 , 5 , 0 , 2 , 0 , 0 ],
                       [2 , 0 , 0 , 0 , 0 , 2 , 0 , 3 , 0 ],
                       [5 , 0 , 0 , 0 , 0 , 0 , 3 , 0 , 5 ],
                       [4 , 1 , 0 , 0 , 0 , 0 , 0 , 5 , 0 ],])

# 将邻接矩阵转换为稀疏矩阵
adj_sparse = csr_matrix(adj_matrix)

# 计算最小生成树
mst = minimum_spanning_tree(adj_sparse)

# 输出最小生成树的邻接矩阵
print("最小生成树的邻接矩阵：")
print(mst.toarray().astype(int))

# 计算最短路径
dist_matrix, predecessors = dijkstra(csgraph=adj_sparse, return_predecessors=True)

# 输出最短路径的距离矩阵和前驱矩阵
print("\n最短路径的距离矩阵：")
print(dist_matrix)

print("\n前驱矩阵：")
print(predecessors)
