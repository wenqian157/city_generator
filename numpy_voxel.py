import numpy as np

nX = nY = nZ = 100
x = y = z = np.linspace(0, 99, 100)
gridX, gridY, gridZ = np.meshgrid(x, y, z, sparse=True)

nbrPts = 10
marginSpace = 10

minRc = 8  
maxRc = 14 
minRt = 1  
maxRt = 6

voxel_bools_crown = np.zeros((nX,nY,nZ))
voxel_bools_trunk = np.zeros((nX,nY,nZ))
for i in range(nbrPts):
    x, y, z = np.random.randint(marginSpace, nX - marginSpace, size=3)
    cr = np.random.randint(minRc, maxRc)
    tr = np.random.randint(minRt, maxRt)

    distX = gridX - x
    distY = gridY - y
    distZ = gridZ - z

    voxel_bools_crown += distX**2 + distY**2 + distZ**2 < cr**2
    voxel_bools_trunk += np.logical_and((distX**2 + distY**2) < tr**2, gridZ < z)

# voxel_bools_crown = voxel_bools_crown != 0
# voxel_bools_trunk = voxel_bools_trunk != 0


voxel_colors_crown = np.repeat(voxel_bools_crown, 3).reshape((100,100,100,3))
# voxel_colors_crown = voxel_colors_crown.astype(np.float32, casting='unsafe')
voxel_colors_crown *= (0.44, 0.54, 0.2)

voxel_colors_trunk = np.repeat(voxel_bools_trunk, 3).reshape((100,100,100,3))
# voxel_colors_trunk = voxel_colors_trunk.astype(np.float32, casting='unsafe')
voxel_colors_trunk *= (0.52,0.34,0.14)

voxel_bools = voxel_bools_crown + voxel_bools_trunk
voxel_colors = voxel_colors_crown + voxel_colors_trunk

# mesh= mola.numpy_to_voxel_mesh(voxel_bools, voxel_colors)
# mesh.normalise_to_dim(20)
# HTML(mola.colab3D.display_mesh(mesh))