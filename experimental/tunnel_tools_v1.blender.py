bl_info = {
    "name": "Tunnel Tools (grid double half shortcuts and other personal tools primarily for level development",
    "author": "Richard Ellicott",
    "blender": (2, 80, 0),
    "category": "Object",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "category": "User Interface",
    "wiki_url": "https://github.com/RichardEllicott/GodotSnippets/",
    "support": "COMMUNITY"
}
# "name": "Grid Scale Double/Half Shotcuts",
# "description": "binds + and - to double and half the grid",
# "author": "Richard Ellicott",
# "version": (1, 0),
# "blender": (2, 80, 0),
# # "location": "View3D > Add > Mesh",
# # "warning": "", # used for warning icon and text in addons panel
# # "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"
# #             "Scripts/My_Script",
# # "tracker_url": "https://developer.blender.org/maniphest/task/edit/form/2/",
# #
# "category": "Object",


"""
https://github.com/RichardEllicott/GodotSnippets/



Plugin Info:

Tunnel Tools v 1.0 EXPERIMENTAL VERSION (WARNING THIS IS A VERY WHISTICAL COLLECTION OF SHORTCUTS THAT I KEEP ALL IN ONE PLACE)


Blender addon that adds shortcuts to blender to double and half the grid scale similar to Doom/Quake level editors

shortcuts are assigned to NUMPAD_PLUS and NUMPAD_MINUS keys, usually they are redundant for zooming next to the mouse wheel


To make usage more intuitive, set the scenes units to "None", set the grid subdivisions to a number like 8.



based on templates:

https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html

coded by Richard Ellicott (https://github.com/RichardEllicott/)


Code is a bit messy because i want to preserve the boilerplate code, however this addon is tested and in my usage.
You're welcome to tidy it if you wish :)



This is my best Blender template to add tests to as it can be loaded as a script in blender itself
Then you can just edit and reload.


All added functions:
    -double grid scale
    -half grid scale
    -origin to base # move object origin
    -origin to corner

    -Append Object Name -col # for usage with godot import, will add the tag for a static body in Godot
        -an easy Blender recipe for Godot export (this is why i use this shortcut)
        -make your models, select them all
        -run this script to append
        -export a DAE on only selected objects (apply modifiers to)
        -now finished, press undo to remove the annoying -col tag

    -Another version of the above will add the -col or -rigidbody if the object has a Blender rigidbody
    -Another tool to set up modifiers




Dev issue notes:
-originally i couldn't get the edit mode shortcuts working, i found "Screen Edit" to be the keyword given in the key preferences
-still some boilerplate code save to make a working menu
-a hack was needed to obtain the active UI window for the grid

creating a panel menu thing: https://blender.stackexchange.com/questions/57306/how-to-create-a-custom-ui


"""


import bpy
import sys
from mathutils import Matrix, Vector
from collections import defaultdict

print("\n" * 4)

print("loading my_grid_double_shortcut_addon.blender2...")


def add_library_search_path(path):
    if not path in sys.path:
        sys.path.append(path)


# load Blender ICE Library...
add_library_search_path("/Users/rich/Documents/GitHub/myrepos/BlenderSnippets/experimental")

import blender_ice_library as ice

import importlib  # import internals
importlib.reload(ice)  # force reload


# Preferences:
# TODO https://docs.blender.org/api/blender_python_api_2_68_release/bpy.types.AddonPreferences.html
# Preferences menu?

double_key_shortcut = "NUMPAD_PLUS"  # you can change the hot keys here
half_key_shortcut = "NUMPAD_MINUS"

# Begin Plugin

# Functions:


def origin_to_bottom(ob, matrix=Matrix()):
    """
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



def origin_to_corner_rework(ob):
    """

    trying to rework this as i prefer to use in script better

    the optimizations of the original make it only usable on the selected objects

    NOT WORKING

    """

    bbox = [Vector(b) for b in ob.bound_box]

    for i, v in enumerate(bbox):
        print("BOUNDING BOX: {} {}".format(i,v))

    bbox = [Vector(b) for b in ob.bound_box]
    lhc = bbox[0]
    T = Matrix.Translation(-lhc)


    ob.data.transform(T)

    # ob.matrix_world.translation = ob.matrix_world @ lhc # moves to the corner


    


def origin_to_corner():  # on all selected
    """

    of all selected mesh

    # https://blender.stackexchange.com/questions/141248/how-to-set-origin-points-of-multiple-objects-to-a-corner-of-their-bounding-boxes

    note this code is only for ALL SELECTED, this is because it doesn't apply the operation to mesh more than once if they're linked
    (maybe a little ott, so recoding to simple version)

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


def get_3D_area_object():
    """
    get the VIEW_3D area object, to change grid settings etc

    get_area_object().overlay.grid_scale = 2
    get_area_object().overlay.grid_subdivisions = 8

    https://blender.stackexchange.com/questions/154610/how-do-you-programatically-set-grid-scale

    """
    AREA = 'VIEW_3D'
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if not area.type == AREA:
                continue
            for s in area.spaces:
                if s.type == AREA:
                    return s
                    break


def get_grid_scale():
    """
    returns grid scale as a float
    """
    return get_3D_area_object().overlay.grid_scale


def set_grid_scale(scale=1):
    """
    sets the grid scale in the UI
    """
    get_3D_area_object().overlay.grid_scale = scale


def get_grid_subdivisons():
    return get_3D_area_object().overlay.grid_subdivisions


def set_grid_subdivisons(subdivisions=8):
    get_3D_area_object().overlay.grid_subdivisions = subdivisions


def half_grid_scale():
    set_grid_scale(get_grid_scale() / 2.0)


def double_grid_scale():
    set_grid_scale(get_grid_scale() * 2.0)


# Blender Operator Objects:


def set_default_grid_settings():
    """
    automatically sets the scene units to none and the grid subdivisions to 8
    """
    bpy.context.scene.unit_settings.system = 'NONE'
    set_grid_subdivisons(8)


class ObjectDoubleGridScale(bpy.types.Operator):
    """Object Double Grid Scale"""
    # bl_idname = "object.double_grid_scale"
    bl_idname = "edit.double_grid_scale"

    bl_label = "Double Grid Scale"
    bl_options = {'REGISTER', 'UNDO'}

    # total: bpy.props.IntProperty(name="Steps", default=2, min=1, max=100) # was for the shortcut context

    def execute(self, context):
        double_grid_scale()
        set_default_grid_settings()
        return {'FINISHED'}


class ObjectHalfGridScale(bpy.types.Operator):
    """Object Half Grid Scale"""
    # bl_idname = "object.half_grid_scale"
    bl_idname = "edit.half_grid_scale"

    bl_label = "Half Grid Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        set_default_grid_settings()
        half_grid_scale()
        return {'FINISHED'}


class ObjectOriginToBase(bpy.types.Operator):
    """
    for all selected objects move origin to base
    """
    bl_idname = "object.object_origin_to_base"

    bl_label = "Origin To Base"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # dimensions = bpy.context.active_object.dimensions
        # position = bpy.context.active_object.location
        # bpy.context.scene.cursor_location = position
        # bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')

        # https://blender.stackexchange.com/questions/42105/set-origin-to-bottom-center-of-multiple-objects?noredirect=1&lq=1

        for o in bpy.context.selected_objects:
            if o.type == 'MESH':
                origin_to_bottom(o)
                # origin_to_bottom(o, matrix=o.matrix_world) # global

        return {'FINISHED'}


class ObjectOriginToCorner(bpy.types.Operator):
    """
    for all selected objects move origin to base
    """
    bl_idname = "object.object_origin_to_corner"

    bl_label = "Origin To Corner"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        origin_to_corner()
        return {'FINISHED'}


class ObjectTagCol(bpy.types.Operator):
    """
    append object name with tag -col


    designed to be used with Godot which uses various tags to load level data from Blender

    https://docs.godotengine.org/en/stable/getting_started/workflow/assets/importing_scenes.html?highlight=importing%20assets#godot-scene-importer


    """
    bl_idname = "object.object_tag_col"

    bl_label = "Append Object Name -col"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for o in bpy.context.selected_objects:
            if o.type == 'MESH':
                if not o.name.endswith("-col"):
                    o.name = o.name + "-col"  # MAIN BIT

        return {'FINISHED'}


class ObjectTagColIfRB(bpy.types.Operator):
    """
    Objects with Passive rigidbody become Static colliders

    Objects with Active rigidbody become rigidbody colliders


    """
    bl_idname = "object.object_tag_col_ifrb"

    bl_label = "Append Object Name -col (IF RB IS ACTIVE EXPERIMENTAL)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # origin_to_corner()

        for o in bpy.context.selected_objects:
            if o.type == 'MESH':

                if o.rigid_body.enabled:
                    if o.rigid_body.type == "PASSIVE":  # Objects with Passive rigidbody become Static colliders
                        if not o.name.endswith("-col"):
                            o.name = o.name + "-col"

                    elif o.rigid_body.type == "ACTIVE":  # Objects with Active rigidbody become rigidbody colliders
                        o.name = o.name + "-rigid"

        return {'FINISHED'}


class ObjectCopyUVProjectModifier(bpy.types.Operator):
    """
    testing adding modifiers etc

    ['DATA_TRANSFER', 'MESH_CACHE', 'MESH_SEQUENCE_CACHE', 'NORMAL_EDIT', 'WEIGHTED_NORMAL', 'UV_PROJECT', 'UV_WARP', 'VERTEX_WEIGHT_EDIT', 'VERTEX_WEIGHT_MIX', 'VERTEX_WEIGHT_PROXIMITY', 'ARRAY', 'BEVEL', 'BOOLEAN', 'BUILD', 'DECIMATE', 'EDGE_SPLIT', 'MASK', 'MIRROR', 'MULTIRES', 'REMESH', 'SCREW', 'SKIN', 'SOLIDIFY', 'SUBSURF', 'TRIANGULATE', 'WIREFRAME', 'WELD', 'ARMATURE', 'CAST', 'CURVE', 'DISPLACE', 'HOOK', 'LAPLACIANDEFORM', 'LATTICE', 'MESH_DEFORM', 'SHRINKWRAP', 'SIMPLE_DEFORM', 'SMOOTH', 'CORRECTIVE_SMOOTH', 'LAPLACIANSMOOTH', 'SURFACE_DEFORM', 'WARP', 'WAVE', 'CLOTH', 'COLLISION', 'DYNAMIC_PAINT', 'EXPLODE', 'OCEAN', 'PARTICLE_INSTANCE', 'PARTICLE_SYSTEM', 'FLUID', 'SOFT_BODY', 'SURFACE']


    """
    bl_idname = "object.copy_uv_project_modifier"

    bl_label = "Copy UV Project modifier"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("running test script a...")

        for ob in bpy.context.selected_objects:
            if ob.type == 'MESH':
                add_custom_uv_to_ob(ob)


        return {'FINISHED'}



def add_custom_uv_to_ob(ob):
    """
    sets up my custom UV on object

    doesn't change object selection

    """
    GEN_NAME = "UVProjectGen" #name is required to retrieve modifier

    if not GEN_NAME in ob.modifiers:

        ob.modifiers.new(GEN_NAME, type='UV_PROJECT') # THIS STYLE DOESN'T CHANGE THE ACTIVE SELECTED OBJECT
        mod = ob.modifiers[GEN_NAME] # POTENTIAL BUG: THIS MIGHT NOT HAVE THE RIGHT NAME
        mod.projector_count = 6
        mod.projectors[0].object = bpy.data.objects["_1_UVBack"]
        mod.projectors[1].object = bpy.data.objects["_2_UVFront"]
        mod.projectors[2].object = bpy.data.objects["_3_UVBottom"]
        mod.projectors[3].object = bpy.data.objects["_4_UVTop"]
        mod.projectors[4].object = bpy.data.objects["_5_UVLeft"]
        mod.projectors[5].object = bpy.data.objects["_6_UVRight"]
        mod.scale_x = 2.0
        mod.scale_y = 2.0
        mod.show_expanded = False






                

class ObjectTestScriptA(bpy.types.Operator):
    """
    testing adding modifiers etc

    ['DATA_TRANSFER', 'MESH_CACHE', 'MESH_SEQUENCE_CACHE', 'NORMAL_EDIT', 'WEIGHTED_NORMAL', 'UV_PROJECT', 'UV_WARP', 'VERTEX_WEIGHT_EDIT', 'VERTEX_WEIGHT_MIX', 'VERTEX_WEIGHT_PROXIMITY', 'ARRAY', 'BEVEL', 'BOOLEAN', 'BUILD', 'DECIMATE', 'EDGE_SPLIT', 'MASK', 'MIRROR', 'MULTIRES', 'REMESH', 'SCREW', 'SKIN', 'SOLIDIFY', 'SUBSURF', 'TRIANGULATE', 'WIREFRAME', 'WELD', 'ARMATURE', 'CAST', 'CURVE', 'DISPLACE', 'HOOK', 'LAPLACIANDEFORM', 'LATTICE', 'MESH_DEFORM', 'SHRINKWRAP', 'SIMPLE_DEFORM', 'SMOOTH', 'CORRECTIVE_SMOOTH', 'LAPLACIANSMOOTH', 'SURFACE_DEFORM', 'WARP', 'WAVE', 'CLOTH', 'COLLISION', 'DYNAMIC_PAINT', 'EXPLODE', 'OCEAN', 'PARTICLE_INSTANCE', 'PARTICLE_SYSTEM', 'FLUID', 'SOFT_BODY', 'SURFACE']


    """
    bl_idname = "object.test_script_a"

    bl_label = "Test Script A"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("running test script a...")

        return {'FINISHED'}


def menu_func(self, context):  # not used atm
    self.layout.operator(ObjectDoubleGridScale.bl_idname)


# store keymaps here to access after registration
addon_keymaps = []


register_list = [
    ObjectDoubleGridScale,
    ObjectHalfGridScale,
    ObjectOriginToBase,
    ObjectOriginToCorner,
    ObjectTagCol,
    ObjectTagColIfRB,

    ObjectCopyUVProjectModifier,

    ObjectTestScriptA
]


def register():

    for ob in register_list:
        bpy.utils.register_class(ob)

    # bpy.types.VIEW3D_MT_object.append(menu_func) # this code would add a menu

    # handle the keymap
    wm = bpy.context.window_manager
    # Note that in background mode (no GUI available), keyconfigs are not available either,
    # so we have to check this to avoid nasty errors in background case.
    kc = wm.keyconfigs.addon
    if kc:
        object_mode_keys = wm.keyconfigs.addon.keymaps.new(name='Screen Editing', space_type='EMPTY')  # name='Object Mode'

        kmi1 = object_mode_keys.keymap_items.new(ObjectDoubleGridScale.bl_idname, double_key_shortcut, 'PRESS')  # double key
        kmi2 = object_mode_keys.keymap_items.new(ObjectHalfGridScale.bl_idname, half_key_shortcut, 'PRESS')  # half key

        # kmi.properties.total = 4 # not needed ?!?!?! https://devtalk.blender.org/t/official-keymap-example-does-not-work/9032

        addon_keymaps.append((object_mode_keys, kmi1))  # saved so we can unregister
        addon_keymaps.append((object_mode_keys, kmi2))  # saved so we can unregister


def unregister():
    # Note: when unregistering, it's usually good practice to do it in reverse order you registered.
    # Can avoid strange issues like keymap still referring to operators already unregistered...
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    for ob in register_list:
        bpy.utils.unregister_class(ob)

    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
