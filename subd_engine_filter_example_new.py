import sys
import os
import random

from sympy import Not

SCRIPT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.dirname(SCRIPT_DIR))
import mola 
# from mola import filter
# from mola import selector

mesh_city = mola.Mesh()

a = mesh_city.add_vertex(0, 0, 0)
b = mesh_city.add_vertex(274, 0, 0)
c = mesh_city.add_vertex(274, 80, 0)
d = mesh_city.add_vertex(0, 80, 0)
mesh_city.add_face([a, b, c, d])

engine = mola.Engine()
# print(engine.successor_rules)

def my_filter(face):
    return face.area() > 100

# filtered = filter(Not(my_filter), mesh_city.faces)
# print(list(filtered))

mesh_city.faces = engine.subdivide(mesh_city.faces, my_filter, 1.0, "face_extrude_tapered", 0, 0.4)

# # filter
# # takes one face, returns boolean
# filter_a = filter("group", "==", "block")
# print(filter_a(mesh_city.faces[0]))

# filter_b = filter("face_area", ">", 1000)
# print(filter_b(mesh_city.faces[0]))

# filter_c = filter("face_angle_vertical", "<", 3)
# print(filter_c(mesh_city.faces[0]))


# # selector
# # takes a list of faces, returns selected faces and unselected faces
# print(selector(mesh_city.faces, filter_a, 1.0))


