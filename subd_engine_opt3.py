import sys
import os
import random

SCRIPT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.dirname(SCRIPT_DIR))
import mola 
from mola import filter
from mola import selector
from mola import Engine

mesh_city = mola.Mesh()

a = mesh_city.add_vertex(0, 0, 0)
b = mesh_city.add_vertex(274, 0, 0)
c = mesh_city.add_vertex(274, 80, 0)
d = mesh_city.add_vertex(0, 80, 0)
mesh_city.add_face([a, b, c, d])

engine = mola.Engine()
# print(engine.successor_rules)

filter1 = filter("group", "==", "block")
filter2 = filter("group", "==", "plot")
filter3 = filter("group", "==", "construct_up")
filter4 = filter("group", "==", "construct_side")
filter5 = filter("group", "==", "wall")
filter6 = filter("group", "==", "panel")
filter7 = filter("group", "==", "roof")

engine.change_face_group(mesh_city.faces, "all", "block")
mesh_city.faces = engine.subdivide(selector(mesh_city.faces, filter1, 1.0), "face_extrude_tapered", 0, 0.4)
mesh_city.faces = engine.subdivide(selector(mesh_city.faces, filter1, 1.0), "mesh_catmull")
mesh_city.faces = engine.subdivide(selector(mesh_city.faces, filter1, 0.95), "face_split_grid", 2, 1)
mesh_city.faces = engine.subdivide(selector(mesh_city.faces, filter1, 0.95), "face_split_grid", 1, 2)

# print(engine.successor_rules["block"])

engine.change_face_group(mesh_city.faces, "block", "plot")
mesh_city.faces = engine.subdivide(selector(mesh_city.faces, filter2, 0.95), "face_extrude_tapered", 0, 0.4, group=True)
for _ in range(10):
    mesh_city.faces = engine.subdivide(selector(mesh_city.faces, filter3, 0.8), "face_extrude_tapered", 5, 0, group=True)

engine.change_face_group(mesh_city.faces, "construct_up", "roof")
engine.change_face_group(mesh_city.faces, "construct_side", "wall")
mesh_city.faces = engine.subdivide(selector(mesh_city.faces, filter5, 1.0), "face_split_cell", 2, 2, group=True)
mesh_city.faces = engine.subdivide(selector(mesh_city.faces, filter6, 0.2), "face_extrude_tapered", 0, 0.3, group=True)
mesh_city.faces = engine.subdivide(selector(mesh_city.faces, filter7, 0.8), "face_extrude_to_point_center", 10)
mesh_city.faces = engine.subdivide(selector(mesh_city.faces, filter7, 0.8), "face_extrude_to_point_center", 3)

print(len(mesh_city.faces))
mola.export_obj(mesh_city, "my_city6b.obj")

