import mola
import random
import citymesh
import math


def group_mesh(mesh):
    for f in mesh.faces:
        angle_v = mola.face_angle_vertical(f)
        if abs(angle_v) <= math.pi * 0.4:  # 0.5 is flat
            f.group = "vertical"
            f.color = (0, 1, 0, 1)
        elif angle_v > math.pi * 0.4:
            f.group = "up"
            f.color = (1, 0, 0, 1)
        else:
            f.group = "down"
            f.color = (0, 0, 0, 1)

    return mesh


def subd_by_group(mesh):
    newMesh = mola.Mesh()
    for f in mesh.faces:
        if f.group == "up":
            if random.random() > 0.6:
                fraction = (random.random() - 0.5) * 0.3
                newFaces = mola.subdivide_face_extrude_tapered(f, 5, fraction)
            else:
                newFaces = [f]
        elif f.group == "vertical":
            if random.random() > 0.97:
                fraction = (random.random() - 0.5) * 0.3
                newFaces = mola.subdivide_face_extrude_tapered(f, 5, fraction)
            else:
                newFaces = [f]
        else:
            newFaces = [f]

        newMesh.faces.extend(newFaces)
    mesh = newMesh
    return mesh


my_city = citymesh.my_city

for i in range(10):
    my_city = group_mesh(my_city)
    my_city = subd_by_group(my_city)
    my_city = group_mesh(my_city)

mola.export_obj(my_city, "my_city.obj")
