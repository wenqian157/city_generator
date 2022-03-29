import sys
import os
import random

SCRIPT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.dirname(SCRIPT_DIR))
import mola 

mesh_city = mola.Mesh()

a = mesh_city.add_vertex(0, 0, 0)
b = mesh_city.add_vertex(274, 0, 0)
c = mesh_city.add_vertex(274, 80, 0)
d = mesh_city.add_vertex(0, 80, 0)
mesh_city.add_face([a, b, c, d])

engine = mola.Engine(mesh_city)

engine.rules.append([{"select":"block", "ratio": 1.0}, {"subd": "face_split_grid", "arg": [2, 1]}])
engine.rules.append([{"select":"block_s", "ratio": 1.0}, {"subd": "face_extrude_to_point_center", "arg": [0]}])
engine.rules.append([{"select":"block_ss", "ratio": 1.0}, {"subd": "mesh_catmull", "arg": []}])

engine.rules.append([{"select":"plot", "ratio": 0.95}, {"subd": "face_extrude_tapered", "arg": [0, 0.4]}])
engine.rules.append([{"select":"construct_up", "ratio": 0.85}, {"subd": "face_extrude_tapered", "arg": [5, 0]}])
engine.rules.append([{"select":"construct_side", "ratio": 0.1}, {"subd": "face_extrude_tapered", "arg": [5, 0]}])
# engine.rules.append([{"select":"wall", "ratio": 1.0}, {"subd": "face_split_cell", "arg": [2, 2]}])
# engine.rules.append([{"select":"panel", "ratio": 0.2}, {"subd": "face_extrude_tapered", "arg": [0, 0.3]}])
# engine.rules.append([{"select":"roof", "ratio": 0.8}, {"subd": "face_extrude_to_point_center", "arg": [10]}])
# engine.rules.append([{"select":"roof_s", "ratio": 0.8}, {"subd": "face_extrude_to_point_center", "arg": [3]}])


engine.subdivide_block(3)
engine.subdivide_building(9)
# engine.subdivide_facade(2)

mesh_city = engine.mesh

mesh_city.update_topology()
mesh_city = mola.subdivide_mesh_catmull(mesh_city)
mesh_city = mola.subdivide_mesh_catmull(mesh_city)

# new_mesh = mola.Mesh()
for f in mesh_city.faces:
    if f.group == "construct_side":
        f.group = "wall"
    elif f.group == "construct_up":
        f.group = "roof"

# left_mesh = mola.Mesh()
# for f in mesh_city.faces:
#     if f.group == "wall" or f.group == "roof":
#         new_mesh.faces.append(f)
#     else:
#         left_mesh.faces.append(f)




new_mesh = mola.Mesh()
for f in mesh_city.faces:
    new_faces = []
    if f.group == "wall":
        new_faces = mola.subdivide_face_split_cell(f, 5, 1)
        for f1 in new_faces:
            f1.group = "facade"
    else:
        new_faces = [f]
    new_mesh.faces.extend(new_faces)
mesh_city = new_mesh

new_mesh = mola.Mesh()
for f in mesh_city.faces:
    new_faces = []
    if f.group == "facade":
        if random.random() > 0.5:
            new_faces = mola.subdivide_face_extrude_tapered(f, 0, 0.3)
            new_faces[-1].group = "glass"
            new_faces[-1].color = (0.1, 0.1, 0.1, 1)
        else:
            new_faces = [f]
    else:
        new_faces = [f]
    new_mesh.faces.extend(new_faces)


mesh_city = new_mesh
print(len(mesh_city.faces))
mola.export_obj(mesh_city, "my_city6b.obj")
