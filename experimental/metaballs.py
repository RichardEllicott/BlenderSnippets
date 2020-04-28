import bpy
import random
from mathutils import Vector

import numpy

gen_key = "GEN55_"


_default_material = False



modifiers_template_name = "UVProjectLINK"
modifiers_template = None
for ob in bpy.context.scene.objects:
# for ob in bpy.data.objects:

    if ob.name.startswith(modifiers_template_name):
         modifiers_template = ob
         break

assert(modifiers_template) # ensure the template is present





def get_random_vector(spread=1.0):
    return Vector((random.uniform(-spread, spread),random.uniform(-spread, spread),random.uniform(-spread, spread)))


def get_random_normal_vector(spread=1.0):
    return Vector((numpy.random.normal(0.0, spread),numpy.random.normal(0.0, spread),numpy.random.normal(0.0, spread)))



def create_random_metaballs(number = 16, spread = 32.0):


    for i in range(number):

        #https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html?highlight=numpy%20random%20normal#numpy.random.normal


        # location = get_random_vector(8.0)

        
        location = get_random_normal_vector(spread)

        # radius = 3.0 + numpy.random.normal(0.0, 1.0)
        radius = 1.0


        # location.z = 0.0

        ball = metaball_add(type='BALL', radius=radius, enter_editmode=False, location=location, name=gen_key+"ball")


    # bpy.ops.object.select_all(action='DESELECT')
    select_created_objects()

def metaball_add(**kwargs):  # reflection
    """
    adds name keyword
    """
    name = None
    if "name" in kwargs:
        name = kwargs["name"]
        del(kwargs["name"])

    # need to add the material as a link

    bpy.ops.object.metaball_add(**kwargs)
    ob = bpy.context.active_object
    if name:
        ob.name = name
    return ob


def delete_generated_items():

    for ob in bpy.context.scene.objects:
        if ob.name.startswith(gen_key):
            bpy.data.objects.remove(ob, do_unlink=True)

    pass

def select_created_objects(key=gen_key):
    for ob in bpy.context.scene.objects:
        if ob.name.startswith(key):
            select_object(ob)

def select_object(ob):  # https://devtalk.blender.org/t/selecting-an-object-in-2-8/4177
    ob.select_set(state=True)
    bpy.context.view_layer.objects.active = ob




if __name__ == '__main__':

    print('running script...')

    delete_generated_items()
    
    create_random_metaballs(number=16,spread=16)

        
    
    

