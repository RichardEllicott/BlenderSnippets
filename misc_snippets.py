"""

random unsorted Blender Python snippets


"""


import bpy


def remove_object(ob):
    bpy.data.objects.remove(ob, do_unlink=True)


def remove_keyed_objects(key="GEN10_"):
    """
    remove all objects beginning with a key (used to mark generated objects)

    this is useful if you write a script to generate an object, that deletes it's old copies if they exist
    """
    for ob in bpy.context.scene.objects:
        if key:
            if ob.name.startswith(key):
                bpy.data.objects.remove(ob, do_unlink=True)  # best option to delete, unlink first
        else:
            bpy.data.objects.remove(ob, do_unlink=True)  # best option to delete, unlink first


def select_keyed_objects(key=gen_key):
    """
    select all objects beginning with a key
    """
    for ob in bpy.context.scene.objects:
        if ob.name.startswith(key):
            select_object(ob)


def select_all(): bpy.ops.object.select_all(action='SELECT')


def deselect_all(): bpy.ops.object.select_all(action='DESELECT')


def select_object(ob):  # https://devtalk.blender.org/t/selecting-an-object-in-2-8/4177
    ob.select_set(state=True)
    bpy.context.view_layer.objects.active = ob


def edit_mode():
    bpy.ops.object.mode_set(mode='EDIT')


def object_mode():
    bpy.ops.object.mode_set(mode='OBJECT')


gen_key = "GEN10_"


def primitive_plane_add(**kwargs):  # reflection
    bpy.ops.mesh.primitive_plane_add(**kwargs)  # edit to new standards
    ob = bpy.context.active_object
    ob.name = gen_key + ob.name  # set name
    ob.data.materials.append(default_material)  # add material
    created_objects.append(ob)
    return ob


def primitive_cube_add(**kwargs):
    bpy.ops.mesh.primitive_cube_add(**kwargs)  # edit to new standards
    ob = bpy.context.active_object
    ob.name = gen_key + ob.name  # set name
    ob.data.materials.append(default_material)  # add material
    created_objects.append(ob)
    return ob


def duplicate_object(ob, linked=0):
    """
    duplicate an object, return a ref to the new object
    uses the UI's duplicate function so works the same
    """
    object_mode()
    deselect_all()
    select_object(ob)
    bpy.ops.object.duplicate(linked=linked, mode='TRANSLATION')
    ob = bpy.context.active_object
    created_objects.append(ob)
    return ob


def set_object_dimensions(ob, dimensions=(1, 1, 1)):
    """
    works on an object similar to how the UI does it rescaling an object, but this function is not available in script
    """
    deselect_all()
    select_object(ob)
    object_dimensions = bpy.context.object.dimensions
    for i in range(len(object_dimensions)):
        ob.scale[i] = dimensions[i] / object_dimensions[i]


def apply_transform(location=True, scale=True, rotation=True):
    bpy.ops.object.transform_apply(location=location, scale=scale, rotation=rotation)  # apply transform



def origin_to_bottom(ob, matrix=Matrix()):
    """
    similar to the origin to geometry functions but
    moves an object's origin to the center bottom, this is good for walls, trees, characters etc

    https://blender.stackexchange.com/questions/42105/set-origin-to-bottom-center-of-multiple-objects?noredirect=1&lq=1
    """
    me = ob.data
    mw = ob.matrix_world
    local_verts = [matrix @ Vector(v[:]) for v in ob.bound_box]
    o = sum(local_verts, Vector()) / 8
    o.z = min(v.z for v in local_verts)
    o = matrix.inverted() @ o
    me.transform(Matrix.Translation(-o))

    mw.translation = mw @ o

