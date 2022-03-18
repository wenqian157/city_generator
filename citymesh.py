import mola

# basic setup

my_city = mola.Mesh()
a = my_city.add_vertex(0, 0, 0)
b = my_city.add_vertex(100, 0, 0)
c = my_city.add_vertex(100, 100, 0)
d = my_city.add_vertex(0, 100, 0)

my_city.add_face([a, b, c, d])

# step 1: sbdivide to ct
newMesh = mola.Mesh()
for f in my_city.faces:
    newFaces = mola.subdivide_face_extrude_to_point_center(f, 0)
    newMesh.faces.extend(newFaces)

my_city = newMesh

# basic setup

my_city = mola.Mesh()
a = my_city.add_vertex(0, 0, 0)
b = my_city.add_vertex(100, 0, 0)
c = my_city.add_vertex(100, 100, 0)
d = my_city.add_vertex(0, 100, 0)

my_city.add_face([a, b, c, d])

# step 1: sbdivide to ct
newMesh = mola.Mesh()
for f in my_city.faces:
    newFaces = mola.subdivide_face_extrude_to_point_center(f, 0)
    newMesh.faces.extend(newFaces)

my_city = newMesh

# newMesh = mola.Mesh()
# for f in my_city.faces:
#     newFaces = mola.subdivide_face_split_grid(f, 2, 2)
#     newMesh.faces.extend(newFaces)

# my_city = newMesh

# step 2:catmull
my_city.update_topology()
my_city = mola.subdivide_mesh_catmull(my_city)

# step 3:split grid
newMesh = mola.Mesh()
for f in my_city.faces:
    newFaces = mola.subdivide_face_split_grid(f, 2, 1)
    newMesh.faces.extend(newFaces)

my_city = newMesh

# step 4:make circulation
newMesh = mola.Mesh()
for f in my_city.faces:
    newFaces = mola.subdivide_face_extrude_tapered(f, 0, 0.45)
    newMesh.faces.extend([newFaces[-1]])

my_city = newMesh

print(type(my_city))
# mola.export_obj(my_city, "my_city.obj")
