
import numpy as np
from scipy.sparse.csgraph import dijkstra

# 构建邻接矩阵表示图
adjacency_matrix = np.array([[0,15, 20, 27, 37, 54], 
                             [0, 0, 15, 20, 27, 37],
                             [0, 0,  0, 15, 20, 27], 
                             [0, 0,  0,  0, 20, 27],
                             [0, 0,  0,  0,  0, 27],
                             [0, 0,  0,  0,  0, 0]])

# 使用 dijkstra 函数计算最短路径
dist_matrix, predecessors = dijkstra(adjacency_matrix, return_predecessors=True)

# 获取源节点到目标节点的最短路径长度
source = 0
target = 5
shortest_path_length = dist_matrix[source, target]
print(f"最短路径长度: {shortest_path_length}")

# 获取源节点到目标节点的最短路径
path = [target]
node = target
while node != source:
    node = predecessors[source, node]
    path.append(node)
path.reverse()
print(f"最短路径: {path}")