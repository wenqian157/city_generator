import numpy as np

voxel_bool = np.random.random((2, 2, 2)) > 0.5
# voxel_color = np.zeros((2, 2, 2, 3))

# voxel_color[voxel_bool] = (1, 1, 1)
# print(voxel_bool)
# print(voxel_color)

print(np.zeros((2, 1)))
for index in np.ndindex((2, 1)):
    print(index)
