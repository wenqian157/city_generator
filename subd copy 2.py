import mola
import random
import citymesh
import math


def group_mesh_faces(mesh):
    for f in mesh.faces:
        if f.group == "fixed":
            pass
        else:
            angle_v = mola.face_angle_vertical(f)
            if abs(angle_v) <= math.pi * 0.4:  # 0.5 is flat
                f.group = "vertical"
                f.color = (0, 1, 0, 1)
            elif angle_v > math.pi * 0.4:
                f.group = "up"
                f.color = (1, 0, 0, 1)
            else:
                f.group = "fixed"
                f.color = (0, 0, 0, 1)

    return mesh


def subd_by_group(mesh, subdivide, *args, **kwargs):
    newMesh = mola.Mesh()
    subdivide = getattr(mola, "subdivide_face_" + subdivide)
    for f in mesh.faces:
        if f.group == "up":
            if random.random() > kwargs["up_reduce"]:
                newFaces = subdivide(f, *args)
            else:
                newFaces = [f]
                f.group = "fixed"
                f.color = (1, 0, 0, 1)
        elif f.group == "vertical":
            if random.random() > kwargs["vertical_reduce"]:
                newFaces = subdivide(f, *args)
            else:
                newFaces = [f]
                f.group = "fixed"
                f.color = (0, 1, 0, 1)
        else:
            newFaces = [f]

        newMesh.faces.extend(newFaces)
    return newMesh


def sub_facade(mesh, window_reduce):
    newMesh = mola.Mesh()
    for f in mesh.faces:
        angle_v = mola.face_angle_vertical(f)
        if abs(angle_v) <= math.pi * 0.4:
            newFaces = subd_facade_to_window(f, 2)
            for fi in newFaces:
                if random.random() > window_reduce:
                    newFacei = mola.subdivide_face_extrude_tapered(fi, 0, 0.3, True) # noqa E501
                    newFacei[-1].group = "glass"
                    newFacei[-1].color = (0.1, 0.1, 0.1, 0)

                else:
                    fi.group = "panel"
                    fi.color = (0, 1, 0, 1)
                    newFacei = [fi]
                newMesh.faces.extend(newFacei)
        else:
            newMesh.faces.append(f)

    return newMesh


def subd_facade_to_window(face, size):
    disU = mola.vertex_distance(face.vertices[0], face.vertices[1])
    disV = mola.vertex_distance(face.vertices[1], face.vertices[2])
    dis = [int(a/size) for a in [disU, disV]]

    return mola.subdivide_face_split_grid(face, *dis)


def subd_city(mesh_plot, subd_rules):
    my_city = mesh_plot
    for i in range(subd_rules["iter"]):
        my_city = group_mesh_faces(my_city)
        my_city = subd_by_group(my_city, subd_rules["subd"], *subd_rules["subd_attr"], **subd_rules["dice"])  # noqa E501

    my_city = group_mesh_faces(my_city)
    my_city = sub_facade(my_city, subd_rules["dice"]["windows"])

    return my_city


my_city = citymesh.my_city

subd_rules = {
    "subd": "extrude_tapered",
    "subd_attr": [5, 0],
    "dice": {"up_reduce": 0.3, "vertical_reduce": 0.9, "windows": 0.5},
    "iter": 10
}

my_city = subd_city(my_city, subd_rules)

mola.export_obj(my_city, "my_city7.obj")
