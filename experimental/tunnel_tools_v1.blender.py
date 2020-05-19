# Tunnel Tools v1.0 (Alpha) Addon by Richard Ellicott
# https://github.com/RichardEllicott/GodotSnippets/
# includes many shortcuts, installs as addon or run in script editor
# includes modified boilerplate code that makes it easier to add hot-keys automatically
# see list "register_list" for a list of all the bpy.types.Operator objects added
# objects have an added parameter that contains a dictionary with their keyboard shortcuts allowing for easy keymap setup
# while this code is a tad messy at the moment, it works! (i am using it for my Blender work flow)
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


"""



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
import inspect  # scans for classes
from mathutils import Matrix, Vector, Euler
import math
from collections import defaultdict


# I DONT THINK THIS WORKS IN BLENDER
import inspect
def print_classes():
    # https://stackoverflow.com/questions/1796180/how-can-i-get-a-list-of-all-classes-within-current-module-in-python
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            print(obj, " ++ ", name)







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


def set_automerge(setting):
    # ob = get_3D_area_object()
    bpy.context.tool_settings.use_mesh_automerge = setting


def get_automerge():
    return bpy.context.tool_settings.use_mesh_automerge


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

def select_all(): bpy.ops.object.select_all(action='SELECT')  # select all


def deselect_all(): bpy.ops.object.select_all(action='DESELECT')  # deselect all


def select_object(ob):  # https://devtalk.blender.org/t/selecting-an-object-in-2-8/4177
    ob.select_set(state=True)
    bpy.context.view_layer.objects.active = ob

# Blender Operator Objects:


def set_default_grid_settings():
    """
    automatically sets the scene units to none and the grid subdivisions to 8

    it's a bit of a hack to make my life easier, may be annoying
    """
    bpy.context.scene.unit_settings.system = 'NONE'
    set_grid_subdivisons(8)


class ObjectAutoMergeToggle(bpy.types.Operator):
    """
    Adding a shortcut for auto merge vertices
    """
    # bl_idname = "object.double_grid_scale"
    bl_idname = "edit.auto_merge_toggle"

    bl_label = "Auto Merge Vertices"
    bl_options = {'REGISTER', 'UNDO'}

    # total: bpy.props.IntProperty(name="Steps", default=2, min=1, max=100) # was for the shortcut context

    def execute(self, context):
        set_automerge(not get_automerge())  # toggle

        return {'FINISHED'}


class ObjectDoubleGridScale(bpy.types.Operator):
    """Object Double Grid Scale"""
    # bl_idname = "object.double_grid_scale"
    bl_idname = "edit.double_grid_scale"

    bl_label = "Double Grid Scale"
    bl_options = {'REGISTER', 'UNDO'}

    screen_editing_hotkey = {
        # NUMPAD_PLUS RIGHT_BRACKET https://docs.blender.org/api/2.82/bpy.types.KeyMapItem.html#bpy.types.KeyMapItem.type
        "type": "NUMPAD_PLUS",
        "value": 'PRESS'
    }

    # PASTED
    # kmi = km.keymap_items.new(ObjectCursorArray.bl_idname, 'T', 'PRESS', ctrl=True, shift=True)
    # https://docs.blender.org/api/2.82/bpy.types.KeyMapItem.html#bpy.types.KeyMapItem

    # total: bpy.props.IntProperty(name="Steps", default=2, min=1, max=100) # was for the shortcut context

    def execute(self, context):
        double_grid_scale()
        set_default_grid_settings()
        # feedback:
        # https://docs.blender.org/api/blender_python_api_2_75_release/bpy.types.Operator.html?highlight=report#bpy.types.Operator.report
        self.report({"INFO"}, "grid_scale = {}".format(get_grid_scale()))
        return {'FINISHED'}


class ObjectHalfGridScale(bpy.types.Operator):
    """Object Half Grid Scale"""
    bl_idname = "edit.half_grid_scale"

    bl_label = "Half Grid Scale"
    bl_options = {'REGISTER', 'UNDO'}

    # pars listed here: https://docs.blender.org/api/2.82/bpy.types.KeyMapItems.html#bpy.types.KeyMapItems.new
    # https://docs.blender.org/api/2.82/bpy.types.KeyMapItem.html
    screen_editing_hotkey = {
        "type": "NUMPAD_MINUS",  # NUMPAD_MINUS LEFT_BRACKET
        "value": 'PRESS'
    }

    def execute(self, context):
        set_default_grid_settings()
        half_grid_scale()
        self.report({"INFO"}, "grid_scale = {}".format(get_grid_scale()))
        return {'FINISHED'}


class ObjectOriginToBottom(bpy.types.Operator):
    """
    for all selected objects move origin to bottom (middle of the base)
    """
    bl_idname = "object.object_origin_to_bottom"

    bl_label = "Origin to Bottom"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # dimensions = bpy.context.active_object.dimensions
        # position = bpy.context.active_object.location
        # bpy.context.scene.cursor_location = position
        # bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')

        # https://blender.stackexchange.com/questions/42105/set-origin-to-bottom-center-of-multiple-objects?noredirect=1&lq=1

        for ob in bpy.context.selected_objects:
            if ob.type == 'MESH':
                origin_to_bottom(ob)
                # origin_to_bottom(ob, matrix=ob.matrix_world) # global

        return {'FINISHED'}


class ObjectOriginToCorner(bpy.types.Operator):
    """
    """
    bl_idname = "object.object_origin_to_corner"

    bl_label = "Origin to Corner (left hand corner)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        origin_to_corner()
        return {'FINISHED'}


class ObjectMoveToPosition(bpy.types.Operator):
    """
    """
    bl_idname = "object.object_move_to_position"

    bl_label = "Move to Position"
    bl_options = {'REGISTER', 'UNDO'}

    # total: bpy.props.IntProperty(name="Steps", default=2, min=1, max=100)  # was for the shortcut context

    # props
    # https://docs.blender.org/api/current/bpy.types.Property.html#bpy.types.Property
    # https://docs.blender.org/api/current/bpy.types.FloatProperty.html#bpy.types.FloatProperty

    # position: bpy.props.FloatProperty(name="position", array_dimensions=3)  # was for the shortcut context
    positionX: bpy.props.FloatProperty(name="positionX")  # was for the shortcut context
    positionY: bpy.props.FloatProperty(name="positionY")  # was for the shortcut context
    positionZ: bpy.props.FloatProperty(name="positionZ")  # was for the shortcut context

    def execute(self, context):

        sel_objs = bpy.context.selected_objects  # get selected objects
        active_ob = bpy.context.view_layer.objects.active

        for ob in sel_objs:

            loc, rot, scale = ob.matrix_world.decompose()
            # self.positionX = loc[0]
            # self.positionY = loc[1]
            # self.positionZ = loc[2]

            print("FOUND: {} {}".format(ob, ob.name))
            print("FOUND: {} ".format(dir(ob)))

            ob.location = (self.positionX, self.positionY, self.positionZ)

        return {'FINISHED'}

def origin_to_center():

    # SAVES THE SELECTED OBJECTS
    sel_objs = bpy.context.selected_objects  # get selected objects
    active_ob = bpy.context.view_layer.objects.active

    bpy.ops.object.select_all(action='DESELECT')  # deselect all

    for ob in sel_objs:
        if ob.type == 'MESH':
            ob.select_set(state=True)  # select the object
            bpy.context.view_layer.objects.active = ob
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')  # only works on selected object

    # RESTORES THE SELECTED OBJECTS
    bpy.ops.object.select_all(action='DESELECT')  # deselect all
    for ob in sel_objs:
        ob.select_set(state=True)  # select
    bpy.context.view_layer.objects.active = active_ob


class ObjectOriginToCenter(bpy.types.Operator):
    """
    for all selected objects move origin to base
    """
    bl_idname = "object.object_origin_to_center"

    bl_label = "Origin to Center"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # for ob in bpy.context.selected_objects:
        #     if ob.type == 'MESH':
        origin_to_center()

        return {'FINISHED'}


class ObjectTagCol(bpy.types.Operator):
    """
    ensure all selected objects end with the -col tag, allowing Godot to generate a static collider


    https://docs.godotengine.org/en/stable/getting_started/workflow/assets/importing_scenes.html?highlight=importing%20assets#godot-scene-importer


    """
    bl_idname = "object.object_tag_col"

    bl_label = "Append Object Name -col"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for ob in bpy.context.selected_objects:
            if ob.type == 'MESH':  # only apply to mesh objects
                if not ob.name.endswith("-col"):  # if already tagged, just ignore

                    ob.name = ob.name.replace("-col", "")  # clean out any other -col tags, sometimes causing issues
                    ob.name = ob.name + "-col"  # -col appended to end so Godot will find it

        return {'FINISHED'}


class ObjectRemoveTagCol(bpy.types.Operator):
    """
    opposite function designed to clear away the -col tags

    """
    bl_idname = "object.object_remove_tag_col"

    bl_label = "Remove Object Name -col"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for ob in bpy.context.selected_objects:
            if ob.type == 'MESH':
                ob.name = ob.name.replace("-col", "")  # removes any existing "-col" sequences in name

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

    bl_label = "Add UV Project Modifier (with default uv projector links)"
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
    GEN_NAME = "UVProjectGen"  # name is required to retrieve modifier

    PROJECTOR_NAMES = [  # names of projectors to add
        "_1_UVBack",
        "_2_UVFront",
        "_3_UVBottom",
        "_4_UVTop",
        "_5_UVLeft",
        "_6_UVRight",
    ]

    SCALE = 2.0

    if not GEN_NAME in ob.modifiers: # if we don't have one already create it
        ob.modifiers.new(GEN_NAME, type='UV_PROJECT')  # THIS STYLE DOESN'T CHANGE THE ACTIVE SELECTED OBJECT

    mod = ob.modifiers[GEN_NAME]  # POTENTIAL BUG: THIS MIGHT NOT HAVE THE RIGHT NAME

    mod.projector_count = len(PROJECTOR_NAMES)  # set camera count
    for (i, v) in enumerate(PROJECTOR_NAMES):
        mod.projectors[i].object = bpy.data.objects[v]  # set all the cameras
    mod.scale_x = SCALE
    mod.scale_y = SCALE
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



class AUTOLOAD_ObjectTestScriptB(bpy.types.Operator):
    """
    """
    bl_idname = "object.test_script_b"

    bl_label = "Test Script B"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("running test script b...")

        return {'FINISHED'}


def menu_func(self, context):  # not used atm
    self.layout.operator(ObjectDoubleGridScale.bl_idname)


# store keymaps here to access after registration
addon_keymaps = []


register_list = [
    ObjectDoubleGridScale,
    ObjectHalfGridScale,

    ObjectOriginToBottom,
    ObjectOriginToCorner,
    ObjectOriginToCenter,

    ObjectTagCol,
    ObjectTagColIfRB,
    ObjectRemoveTagCol,

    ObjectCopyUVProjectModifier,

    ObjectTestScriptA,

    ObjectAutoMergeToggle,

    ObjectMoveToPosition
]


# def load_autoloading_classes():
#     g = globals().copy()
#     for name, obj in g.items():
#         if inspect.isclass(obj):
#             print("FSFSFS ", name)

#             if not obj in register_list:
#                 register_list.append(obj)

# load_autoloading_classes()


def register():

    print("loading tunnel_tools_v1 by Richard Ellicott (https://github.com/RichardEllicott/BlenderSnippets)...")

    print("load operators from register_list ({})".format(register_list))

    for ob in register_list:
        bpy.utils.register_class(ob)

    # bpy.types.VIEW3D_MT_object.append(menu_func) # this code would add a menu

    # handle the keymap
    wm = bpy.context.window_manager
    # Note that in background mode (no GUI available), keyconfigs are not available either,
    # so we have to check this to avoid nasty errors in background case.
    kc = wm.keyconfigs.addon
    if kc:
        screen_editing_keys = wm.keyconfigs.addon.keymaps.new(name='Screen Editing', space_type='EMPTY')  # name='Object Mode'
        # screen_editing_keys = wm.keyconfigs.addon.keymaps.new(name='3D View (Global)', space_type='EMPTY')  # name='Object Mode'

        object_mode_keys = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')  # name='Object Mode'

        # kmi.properties.total = 4 # not needed ?!?!?! https://devtalk.blender.org/t/official-keymap-example-does-not-work/9032

        print("******DEBUG CHUNCK********")
        print(dir())

        for ob in register_list:
            if hasattr(ob, 'screen_editing_hotkey') and ob.screen_editing_hotkey:  # FIND OUR CUSTOM KEY SETUP DICTS

                pars_dict = {"idname": ob.bl_idname}  # building the pars dictionary to load into function
                pars_dict.update(ob.screen_editing_hotkey)
                kmi_A = screen_editing_keys.keymap_items.new(**pars_dict)  # ADD THE ACTUAL KEY (BECOMES LIVE HERE)
                addon_keymaps.append((screen_editing_keys, kmi_A))  # stored for later access (optional)

            if hasattr(ob, 'object_mode_hotkey') and ob.object_mode_hotkey:

                pars_dict = {"idname": ob.bl_idname}
                pars_dict.update(ob.object_mode_hotkey)
                kmi_A = object_mode_keys.keymap_items.new(**pars_dict)
                addon_keymaps.append((object_mode_keys, kmi_A))


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



    # REFLECTION code, will automatically add any classes that begin with "AUTOLOAD"
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            if name.startswith("AUTOLOAD"):
                if not obj in register_list: # if not already in the register list
                    register_list.append(obj) # add it

                    print("OBJECT ADDED TO LIST!!")



    register()
