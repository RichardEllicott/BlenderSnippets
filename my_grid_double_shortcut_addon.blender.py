bl_info = {
    "name": "Grid Scale Double/Half Shotcuts",
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

Details:


GridDoubleScaleHotkeys v 1.0 (finished 26/03/2020)

Blender addon that adds shortcuts to blender to double and half the grid scale similar to Doom level editors

shortcuts are assigned to NUMPAD_PLUS and NUMPAD_MINUS keys, usually they are redundant for zooming next to the mouse wheel


it is suggested to set the grid subdivisions to 8 (for a less confusing look), which to do you must first set the scene properties units to "none" instead of the default (metric)


based on templates:

https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html

coded by Richard Ellicott (https://github.com/RichardEllicott/)






"""


import bpy
from mathutils import Matrix, Vector


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


def set_grid_scale(scale=1):
    """
    sets the grid scale in the UI
    """
    get_3D_area_object().overlay.grid_scale = scale


def get_grid_scale():
    """
    returns grid scale as a float
    """
    return get_3D_area_object().overlay.grid_scale


def set_grid_subdivisons(subdivisions=8):
    get_3D_area_object().overlay.grid_subdivisions = subdivisions


def half_grid_scale():
    # set_grid_subdivisons(8)
    set_grid_scale(get_grid_scale() / 2.0)
    pass


def double_grid_scale():
    # set_grid_subdivisons(8)
    set_grid_scale(get_grid_scale() * 2.0)
    pass


# Blender Operator Objects:

class ObjectDoubleGridScale(bpy.types.Operator):
    """Object Double Grid Scale"""
    # bl_idname = "object.double_grid_scale"
    bl_idname = "edit.double_grid_scale"

    bl_label = "Double Grid Scale"
    bl_options = {'REGISTER', 'UNDO'}

    # total: bpy.props.IntProperty(name="Steps", default=2, min=1, max=100) # was for the shortcut context

    def execute(self, context):

        double_grid_scale()
        # half_grid_scale()

        # scene = context.scene
        # cursor = scene.cursor.location
        # obj = context.active_object

        # for i in range(self.total):
        #     obj_new = obj.copy()
        #     scene.collection.objects.link(obj_new)

        #     factor = i / self.total
        #     obj_new.location = (obj.location * factor) + (cursor * (1.0 - factor))

        return {'FINISHED'}


class ObjectHalfGridScale(bpy.types.Operator):
    """Object Half Grid Scale"""
    # bl_idname = "object.half_grid_scale"
    bl_idname = "edit.half_grid_scale"

    bl_label = "Half Grid Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        half_grid_scale()

        return {'FINISHED'}


class ObjectOriginToBase(bpy.types.Operator):

    """ObjectOriginToBase"""
    bl_idname = "object.object_origin_to_base"

    bl_label = "Object Origin To Base"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # dimensions = bpy.context.active_object.dimensions
        # position = bpy.context.active_object.location
        # bpy.context.scene.cursor_location = position
        # bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')

        origin_to_bottom(bpy.context.active_object)

        return {'FINISHED'}

    pass


def menu_func(self, context):  # used atm
    self.layout.operator(ObjectDoubleGridScale.bl_idname)


# store keymaps here to access after registration
addon_keymaps = []


register_list = [
    ObjectDoubleGridScale,
    ObjectHalfGridScale,
    ObjectOriginToBase
]


def register():

    for ob in register_list:
        bpy.utils.register_class(ob)

    # bpy.types.VIEW3D_MT_object.append(menu_func) # don't add to object menu!

    # handle the keymap
    wm = bpy.context.window_manager
    # Note that in background mode (no GUI available), keyconfigs are not available either,
    # so we have to check this to avoid nasty errors in background case.
    kc = wm.keyconfigs.addon
    if kc:
        object_mode_keys = wm.keyconfigs.addon.keymaps.new(name='Screen Editing', space_type='EMPTY') #name='Object Mode'
        # kmi = km.keymap_items.new(ObjectDoubleGridScale.bl_idname, 'T', 'PRESS', ctrl=True, shift=True) # OLD PAT WITH CTRL SHIFT
        kmi1 = object_mode_keys.keymap_items.new(ObjectDoubleGridScale.bl_idname, double_key_shortcut, 'PRESS')

        kmi2 = object_mode_keys.keymap_items.new(ObjectHalfGridScale.bl_idname, half_key_shortcut, 'PRESS')  # DUPLICATED PATTERN

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

    # bpy.utils.unregister_class(ObjectDoubleGridScale) # REPLACED WITH LIST PATTERN
    # bpy.utils.unregister_class(ObjectHalfGridScale) # DUPLICATED PATTERN
    # bpy.utils.unregister_class(ObjectOriginToBase) # DUPLICATED PATTERN

    for ob in register_list:
        bpy.utils.unregister_class(ob)

    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
