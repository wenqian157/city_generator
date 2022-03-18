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


def subd_by_group(mesh, subdivide, *args):
    newMesh = mola.Mesh()
    subdivide = getattr(mola, "subdivide_face_" + subdivide)
    for f in mesh.faces:
        if f.group == "up":
            if random.random() > 0.5:
                if args[1] == "random":
                    fraction = (random.random() - 0.5) * 0.2
                    newFaces = subdivide(f, args[0], fraction)
                else:
                    newFaces = subdivide(f, *args)
            else:
                newFaces = [f]
        elif f.group == "vertical":
            if random.random() > 0.9:
                if args[1] == "random":
                    fraction = (random.random() - 0.5) * 0.2
                    newFaces = subdivide(f, args[0], fraction)
                else:
                    newFaces = subdivide(f, *args)
            else:
                newFaces = [f]
        else:
            newFaces = [f]

        newMesh.faces.extend(newFaces)
    mesh = newMesh
    return mesh


my_city = citymesh.my_city


subd_rules = {
    0: ["extrude_tapered", [5, 0.2]],
    1: ["split_grid", [2, 1]],
    2: ["extrude_tapered", [5, "random"]],
    3: ["extrude_tapered", [5, 0.1]],
    4: ["split_grid", [2, 1]],
    5: ["extrude_tapered", [5, "random"]],
}

for i in range(len(subd_rules)):
    my_city = group_mesh(my_city)
    my_city = subd_by_group(my_city, subd_rules[i][0], *subd_rules[i][1])
    my_city = group_mesh(my_city)

mola.export_obj(my_city, "my_city2.obj")


mesh = mola.construct_tetrahedron(10)
newMesh = mola.Mesh()
for f in mesh.faces:
    newFaces = mola.subdivide_face_extrude(f, 2, capTop=False)
    newMesh.faces.extend(newFaces)
mesh = newMesh
