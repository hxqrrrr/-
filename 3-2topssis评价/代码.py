import numpy as np
from scipy.spatial.distance import euclidean

def topsis(matrix, weights, normalization='vector'):
    # Step 1: Normalize the decision matrix
    if normalization == 'vector':
        norm_matrix = matrix / np.sqrt((matrix**2).sum(axis=0))
    elif normalization == 'max':
        norm_matrix = matrix / matrix.max(axis=0)
    else:
        raise ValueError("Unsupported normalization method")

    # Step 2: Weight the normalized decision matrix
    weighted_matrix = norm_matrix * weights

    # Step 3: Determine the ideal and negative-ideal solutions
    ideal_solution = np.max(weighted_matrix, axis=0)
    negative_ideal_solution = np.min(weighted_matrix, axis=0)

    # Step 4: Calculate the distance to the ideal and negative-ideal solutions
    distance_to_ideal = np.apply_along_axis(euclidean, 1, weighted_matrix, ideal_solution)
    distance_to_negative_ideal = np.apply_along_axis(euclidean, 1, weighted_matrix, negative_ideal_solution)

    # Step 5: Calculate the relative closeness to the ideal solution
    relative_closeness = distance_to_negative_ideal / (distance_to_ideal + distance_to_negative_ideal)

    # Step 6: Rank the alternatives
    rankings = np.argsort(relative_closeness)[::-1]

    return relative_closeness, rankings

# 示例数据
decision_matrix = np.array([
    [250, 16, 12, 5],
    [200, 16, 8, 3],
    [300, 32, 16, 4],
    [275, 32, 8, 4],
    [225, 16, 16, 2]
])

weights = np.array([0.25, 0.25, 0.25, 0.25])

# 调用TOPSIS方法
relative_closeness, rankings = topsis(decision_matrix, weights)

print("Relative Closeness:", relative_closeness)
print("Rankings:", rankings)
