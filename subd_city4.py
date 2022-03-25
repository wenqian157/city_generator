import sys
import os

SCRIPT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.dirname(SCRIPT_DIR))
import mola 

mesh_city = mola.Mesh()

a = mesh_city.add_vertex(0, 0, 0)
b = mesh_city.add_vertex(100, 0, 0)
c = mesh_city.add_vertex(100, 100, 0)
d = mesh_city.add_vertex(0, 100, 0)
mesh_city.add_face([a, b, c, d])

engine = mola.Engine(mesh_city)


engine.rules.append([{"select":"block", "ratio": 1.0}, {"subd": "face_extrude_to_point_center", "arg": [0]}])
engine.rules.append([{"select":"block_s", "ratio": 1.0}, {"subd": "mesh_catmull", "arg": []}])
engine.rules.append([{"select":"block_ss", "ratio": 0.95}, {"subd": "face_split_grid", "arg": [2, 1]}])
engine.rules.append([{"select":"plot", "ratio": 0.9}, {"subd": "face_extrude_tapered", "arg": [0, 0.3]}])
engine.rules.append([{"select":"construct_up", "ratio": 0.7}, {"subd": "face_extrude_tapered", "arg": [5, 0]}])
engine.rules.append([{"select":"construct_side", "ratio": 0.1}, {"subd": "face_extrude_tapered", "arg": [5, 0]}])
engine.rules.append([{"select":"wall", "ratio": 0.9}, {"subd": "face_split_cell", "arg": [2, 2]}])
engine.rules.append([{"select":"panel", "ratio": 0.5}, {"subd": "face_extrude_tapered", "arg": [0, 0.3]}])

n = 15
for i in range(n):
    if i <=3:
        engine.subdivide_block()
    elif i >= n - 2:
        engine.subdivide_facade()
    else:
        engine.subdivide_building()

# engine.subdivide_block(3)
# engine.subdivide_building(10)
# engine.subdivide_facade(2)

mesh_city = engine.mesh
print(len(mesh_city.faces))
mola.export_obj(mesh_city, "my_city.obj")
