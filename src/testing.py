import numpy as np

matrix = np.zeros(shape=(2, 1))
result = np.append(matrix, [[1], [1]], axis=0)
print(matrix)
print(result)
