bl_info = {
    "name": "Grid Scale Double/Half Shortcuts (plus other scripts)",
    "author": "Richard Ellicott",
    "blender": (2, 80, 0),
    "category": "Object",
    "version": (2, 101),
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

Plugin Info:

GridDoubleScaleHotkeys v 2.101 EXPERIMENTAL VERSION

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



Dev issue notes:
-originally i couldn't get the edit mode shortcuts working, i found "Screen Edit" to be the keyword given in the key preferences
-still some boilerplate code save to make a working menu
-a hack was needed to obtain the active UI window for the grid

creating a panel menu thing: https://blender.stackexchange.com/questions/57306/how-to-create-a-custom-ui


"""


import bpy
from mathutils import Matrix, Vector
from collections import defaultdict


if bpy.app.version[0] < 2 or bpy.app.version[1] < 8:
    raise Exception("This Triplanar UV mapping addons works only in Blender 2.8 and above")


# Preferences:

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


def origin_to_corner():  # on all selected

    # https://blender.stackexchange.com/questions/141248/how-to-set-origin-points-of-multiple-objects-to-a-corner-of-their-bounding-boxes

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

    bl_label = "Object Origin To Base"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # dimensions = bpy.context.active_object.dimensions
        # position = bpy.context.active_object.location
        # bpy.context.scene.cursor_location = position
        # bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')

        # https://blender.stackexchange.com/questions/42105/set-origin-to-bottom-center-of-multiple-objects?noredirect=1&lq=1

        for o in bpy.context.scene.objects:
            if o.type == 'MESH':
                origin_to_bottom(o)
                # origin_to_bottom(o, matrix=o.matrix_world) # global

        return {'FINISHED'}


class ObjectOriginToCorner(bpy.types.Operator):
    """
    for all selected objects move origin to base
    """
    bl_idname = "object.object_origin_to_corner"

    bl_label = "Object Origin To Corner"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        origin_to_corner()
        return {'FINISHED'}


class ObjectTestScriptA(bpy.types.Operator):
    """
    for all selected objects move origin to base
    """
    bl_idname = "object.test_script_a"

    bl_label = "Test Script A"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("running test script a...")

        bpy.context.scene.unit_settings.system = 'METRIC'
        bpy.context.scene.unit_settings.system = 'NONE'

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
