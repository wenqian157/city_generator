import sys
import os
import random



SCRIPT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.dirname(SCRIPT_DIR))
import mola 
from mola.mesh_subdivison_engine import Engine

mesh_city = mola.Mesh()

a = mesh_city.add_vertex(0, 0, 0)
b = mesh_city.add_vertex(274, 0, 0)
c = mesh_city.add_vertex(274, 80, 0)
d = mesh_city.add_vertex(0, 80, 0)
mesh_city.add_face([a, b, c, d])

# def subdivide(faces, filter, ratio, rule, labling):
#     to_be_divided_faces = []
#     undivided_faces = []
#     unselected_faces = []
#     devidied_faces = []

#     for f in faces:
#         if filter(f):
#             if random.random() < ratio:
#                 to_be_divided_faces.append(f)
#             else:
#                 undivided_faces.append(f)
#         else:
#             unselected_faces.append(f)

#     for f in to_be_divided_faces:
#         devidied_faces.append(rule(f))

#     labling(devidied_faces, undivided_faces)

#     devidied_faces = [face for faces in devidied_faces for face in faces]

#     return devidied_faces + undivided_faces + unselected_faces

# init
for f in mesh_city.faces:
    f.group = "block"

# step1
def my_filter(face):
    return face.group == "block"

def my_rule(face):
    return mola.subdivide_face_extrude_tapered(face, 0, 0.4)

def my_labeling(devided_faces, undevidied_faces):
    for faces in devided_faces:
        for f in faces:
            f.group = "block"
    for f in undevidied_faces:
        f.group = "plaza"

mesh_city.faces = Engine.subdivide(mesh_city.faces, my_filter, 1.0, my_rule, my_labeling)

def my_rule(face):
    return mola.subdivide_face_split_grid(face, 2, 1)

mesh_city.faces = Engine.subdivide(mesh_city.faces, my_filter, 1.0, my_rule, my_labeling)

def my_rule(face):
    return mola.subdivide_face_split_grid(face, 1, 2)

def my_labeling(devided_faces, undevidied_faces):
    for faces in devided_faces:
        for f in faces:
            f.group = "plot"
    for f in undevidied_faces:
        f.group = "plaza"

mesh_city.faces = Engine.subdivide(mesh_city.faces, my_filter, 1.0, my_rule, my_labeling)

def my_filter(face):
    return face.group == "plot"

def my_rule(face):
    return mola.subdivide_face_extrude_tapered(face, 0, 0.4)

def my_labeling(devided_faces, undevidied_faces):
    for faces in devided_faces:
        Engine.group_by_index(faces, "road", "construct_up")

    for f in undevidied_faces:
        f.group = "plaza"

mesh_city.faces = Engine.subdivide(mesh_city.faces, my_filter, 0.9, my_rule, my_labeling)

def my_filter(face):
    return face.group == "construct_up"

def my_rule(face):
    return mola.subdivide_face_extrude_tapered(face, 5, 0)

def my_labeling(devided_faces, undevidied_faces):
    for faces in devided_faces:
        Engine.group_by_orientation(faces, "construct_up", "construct_down", "construct_side")
    for f in undevidied_faces:
        f.group = "roof"

for _ in range(6):
    mesh_city.faces = Engine.subdivide(mesh_city.faces, my_filter, 0.8, my_rule, my_labeling)

for f in mesh_city.faces:
    if f.group == "construct_up":
        f.group = "roof"
    elif f.group == "construct_side":
        f.group = "wall"

def my_filter(face):
    return face.group == "wall"

def my_rule(face):
    return mola.subdivide_face_split_cell(face, 2, 2)

def my_labeling(devided_faces, undevidied_faces):
    for faces in devided_faces:
        Engine.group_by_default(faces, "panel")
    for f in undevidied_faces:
        f.group = "facade"

mesh_city.faces = Engine.subdivide(mesh_city.faces, my_filter, 0.9, my_rule, my_labeling)

def my_filter(face):
    return face.group == "panel"

def my_rule(face):
    return mola.subdivide_face_extrude_tapered(face, 0, 0.3)

def my_labeling(devided_faces, undevidied_faces):
    for faces in devided_faces:
        Engine.group_by_index(faces, "frame", "glass")
    for f in undevidied_faces:
        f.group = "brick"

mesh_city.faces = Engine.subdivide(mesh_city.faces, my_filter, 0.2, my_rule, my_labeling)

def my_filter(face):
    return face.group == "roof"

def my_rule(face):
    return mola.subdivide_face_extrude_to_point_center(face, 10)

def my_labeling(devided_faces, undevidied_faces):
    for faces in devided_faces:
        Engine.group_by_default(faces, "roof")
    for f in undevidied_faces:
        f.group = "roof"

mesh_city.faces = Engine.subdivide(mesh_city.faces, my_filter, 0.8, my_rule, my_labeling)

def my_rule(face):
    return mola.subdivide_face_extrude_to_point_center(face, 3)

mesh_city.faces = Engine.subdivide(mesh_city.faces, my_filter, 0.8, my_rule, my_labeling)

# for f in mesh_city.faces:
#     print(f.group)

Engine.color_by_group(mesh_city.faces)

mola.export_obj(mesh_city, "my_city.obj")