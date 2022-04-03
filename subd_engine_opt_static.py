import sys
import os
import random

SCRIPT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.dirname(SCRIPT_DIR))
import mola 
from mola import filter
from mola import selector
from mola import Engine

mesh_city = mola.Engine()

a = mesh_city.add_vertex(0, 0, 0)
b = mesh_city.add_vertex(274, 0, 0)
c = mesh_city.add_vertex(274, 80, 0)
d = mesh_city.add_vertex(0, 80, 0)
mesh_city.add_face([a, b, c, d])

# OPT1
filter1 = filter("group", "==", "block")
filter2 = filter("group", "==", "plot")
filter3 = filter("group", "==", "construct_up")
filter4 = filter("group", "==", "construct_side")
filter5 = filter("group", "==", "wall")
filter6 = filter("group", "==", "panel")
filter7 = filter("group", "==", "roof")

mesh_city.face_to_block()
mesh_city.faces = Engine.subdivide(selector(mesh_city.faces, filter1, 1.0), "face_split_grid", 2, 1)
mesh_city.faces = Engine.subdivide(selector(mesh_city.faces, filter1, 1.0), "face_extrude_to_point_center", 0)
mesh_city.faces = Engine.subdivide(selector(mesh_city.faces, filter1, 1.0), "mesh_catmull")

# print(mesh_city.successor_rules["block"])

mesh_city.block_to_plot()
mesh_city.faces = Engine.subdivide(selector(mesh_city.faces, filter2, 0.9), "face_extrude_tapered", 0, 0.3, group=True)
for _ in range(10):
    mesh_city.faces = Engine.subdivide(selector(mesh_city.faces, filter3, 0.7), "face_extrude_tapered", 5, 0, group=True)
    mesh_city.faces = Engine.subdivide(selector(mesh_city.faces, filter4, 0.1), "face_extrude_tapered", 5, 0, group=True)

mesh_city.construct_to_facade()
mesh_city.faces = Engine.subdivide(selector(mesh_city.faces, filter5, 0.9), "face_split_cell", 2, 2, group=True)
mesh_city.faces = Engine.subdivide(selector(mesh_city.faces, filter6, 0.5), "face_extrude_tapered", 0, 0.2, group=True)
mesh_city.faces = Engine.subdivide(selector(mesh_city.faces, filter7, 0.8), "face_extrude_to_point_center", 10)
mesh_city.faces = Engine.subdivide(selector(mesh_city.faces, filter7, 0.8), "face_extrude_to_point_center", 3)

print(len(mesh_city.faces))
mola.export_obj(mesh_city, "my_city6b.obj")

