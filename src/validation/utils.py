import numpy as np

def groups(number, size):
    groups = np.zeros(shape=(0, 0))
    occurance = int(round(size / number))
    for i in range(number):
        groups = np.append(groups, np.array([i] * occurance))
    if (size > groups.size):
        to_add = size - groups.size
        groups = np.append(groups, np.array([0] * to_add))
    return groups
