import sys
import os
import random

import operator


SCRIPT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.dirname(SCRIPT_DIR))
import mola 

mesh_city = mola.Engine()

a = mesh_city.add_vertex(0, 0, 0)
b = mesh_city.add_vertex(274, 0, 0)
c = mesh_city.add_vertex(274, 80, 0)
d = mesh_city.add_vertex(0, 80, 0)
mesh_city.add_face([a, b, c, d])


def filter(attr, relate, arg):
    ops = {'>': operator.gt,
           '<': operator.lt,
           '>=': operator.ge,
           '<=': operator.le,
           '==': operator.eq}

    return lambda f: ops[relate](getattr(f, attr), arg)


def selector(faces, filter, ratio):
    selected = []
    unselected = []
    for f in faces:
        if filter(f):
            if random.random() < ratio:
                selected.append(f)
            else:
                unselected.append(f)
        else:
            unselected.append(f)
    
    return selected, unselected


filter_a = filter("group", "==", "block")

print(selector(mesh_city.faces, filter_a, 1.0))

