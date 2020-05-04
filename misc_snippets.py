"""

random unsorted Blender Python snippets


"""


import bpy


selected_object = bpy.context.active_object

# iterate scene objects
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        print(o)

# iterate selected objects
for o in bpy.context.selected_objects:
    # all objects (lights etc)
    if o.type == 'MESH':
        # just mesh
        print(o)


# iterate modifiers
for modifier in selected_object.modifiers:
    print("{} {}".format(mod,type(mod)))

# print modifiers
print([modifier.identifier for modifier in bpy.types.Modifier.bl_rna.properties['type'].enum_items])


# get object transform
loc, rot, scale = ob.matrix_world.decompose()

# rotate object euler:
ob.rotation_euler = Euler((0.3, 0.3, 0.4), 'XYZ') # rotate object test




def apply_to_selected_objects(fun, *args, **kwargs):
    """
    https://blender.stackexchange.com/questions/129955/looping-through-selected-objects-one-at-a-time
    """
    sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH'] # get selected objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in sel_objs:
        bpy.context.view_layer.objects.active = obj
        yield fun(obj, *args, **kwargs)





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


def select_all(): bpy.ops.object.select_all(action='SELECT') # select all


def deselect_all(): bpy.ops.object.select_all(action='DESELECT') # deselect all


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



def origin_to_corner(): # on all selected
    """

    another setup i find useful, put all the origins to the bottom left hand corner

    that the one where the axis arrows essentially originate from, (-1.0, -1.0, -1.0) on the bounding box

    this is useful for things lining up to the grid, walls, floors etc

    https://blender.stackexchange.com/questions/141248/how-to-set-origin-points-of-multiple-objects-to-a-corner-of-their-bounding-boxes


    """


    context = bpy.context

    meshobs = defaultdict(list)
    for o in context.selected_objects:
        if o.type == 'MESH':
            meshobs[o.data].append(o)


    for me, obs in meshobs.items():
        o = obs[0]
        bbox = [Vector(b) for b in o.bound_box]
        lhc = bbox[0]
        T = Matrix.Translation(-lhc)
        me.transform(T)
        for o in obs:
            o.matrix_world.translation = o.matrix_world @ lhc



def add_library_search_path(path):
    """
    add a library search path, also when dealing with libraries, you may want to force a refresh (blenders python is an open session):

    import importlib # import internals
    importlib.reload(ice) # force reload
    """
    if not path in sys.path:
        sys.path.append(path)




