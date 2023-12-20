"""



"""
import bpy
import sys

print("loading Blender ICE Library test...")




def add_library_search_path(path):
    if not path in sys.path:
        sys.path.append(path)
add_library_search_path("/Users/rich/Documents/GitHub/myrepos/BlenderSnippets/experimental")

import blender_ice_library
import importlib # import internals
importlib.reload(blender_ice_library) # force reload # forces a refresh, in-case of editing this library


from blender_ice_library import *


gen_key = "GEN27_"







if __name__ == "__main__":
    print("blender_ice_library_test.py")

    ball = ice.metaball_add(type='BALL', radius=1.0, enter_editmode=False, location=math.get_random_normal_vector(16.0), name=gen_key+"ball")
    print("generated link to ball: {} {}".format(ball, ball.name))

    ui.grid_scale = 2.0



