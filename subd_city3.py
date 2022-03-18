import re
import sys
import os
import random
import math
from webbrowser import get

SCRIPT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.dirname(SCRIPT_DIR))
import mola 
import citymesh

# Engine.subdivide(
# {
# {my_selector,rule}
# {my_selector,rule}
# {my_selector,rule}
# {my_selector,rule}
# }
# )


class Engine:
    def __init__(self, mesh):
        self.mesh = mesh
        self.rules = []
        self.color = {
            "grow_up": (1, 0, 0, 1),
            "grow_side": (0, 1, 0, 1),
            "roof": (1, 0, 0, 1),
            "facade": (0, 1, 0, 1),
            "window": (0.1, 0.1, 0.1, 0),
            "road": (0, 0, 0, 1),
            "others": (0, 0, 0, 1)
        }

    def _group_faces(self, faces):
        for f in faces:
            if f.group == "fixed":
                pass
            else:
                angle_v = mola.face_angle_vertical(f)
                if abs(angle_v) <= math.pi * 0.4:  # 0.5 is flat
                    f.group = "grow_side"
                    f.color = (0, 1, 0, 1)
                elif angle_v > math.pi * 0.4:
                    f.group = "grow_up"
                    f.color = (1, 0, 0, 1)
                else:
                    f.group = "fixed"
                    f.color = (0, 0, 0, 1)

        return faces
    
    def _group_glass_frame():
        pass

    def _group_plot_road():
        pass

    def _group_grow_up_side():
        pass

    def group_mesh_faces(self):
        self.mesh.faces = self._group_faces(self.mesh.faces)

    def subdivide(self, iter):
        for _ in range(iter):
            for rule in self.rules:
                for i in len(rule):
                    newMesh = mola.Mesh()
                    subd = rule[1]["subd"][i]
                    args = rule[1]["arg"][i]
                    
                    if subd == "mesh_catmull":
                        self.mesh.update_topology()

                    subdivide = getattr(mola, "subdivide_" + subd)
                    for f in self.mesh.faces:
                        if f.group == rule[0]["select_from"]:
                            if random.random() < rule[0]["ratio"]:
                                newFaces = subdivide(f, *args)
                                newFaces = self._group_faces(newFaces)
                            else:
                                newFaces = [f]
                                f.group = rule[0]["left"]
                        else:
                            newFaces = [f]
                        newMesh.faces.extend(newFaces)
                    self.mesh = newMesh

            

selector1 = {"select_from":"grow_up", "ratio": 0.9, "left": "roof"}
rule1 = {"subd": ["face_extrude_tapered"], "arg": [[5, 0, True]]}

selector2 = {"select_from":"grow_side", "ratio": 0.1, "left": "facade"}
rule2 = {"subd": ["face_extrude_tapered"], "arg": [[5, 0, True]]}

selector3 = {"select_from":"facade", "ratio": 0.5, "left": "panel"}
rule3 = {"subd": ["face_extrude_tapered"], "arg": [[0, 0.3, True]]}

selector3 = {"select_from":"roof", "ratio": 0.5, "left": ""}
rule3 = {"subd": ["face_extrude_to_point_center"], "arg": [[5]]}

selector4 = {"select_from":"block", "ratio": 1.0, "left": ""}
rule4 = {"subd": ["face_extrude_to_point_center", "mesh_catmull"], "arg": [[0],[]]}

selector5 = {"select_from":"plot", "ratio": 0.9, "left": "park"}
rule5 = {"subd": ["face_split_grid"], "arg": [[2, 1]]}


my_rules = [
    [selector1, rule1],
    [selector2, rule2]
]
mesh = citymesh.my_city
my_engine = Engine(mesh)
my_engine.group_mesh_faces()
my_engine.rules = my_rules
my_engine.subdivide(10)
print(len(my_engine.mesh.faces))