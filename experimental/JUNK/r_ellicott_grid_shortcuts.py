bl_info = {
    "name": "r_ellicott grid shortcuts",
    "author": "Richard Ellicott",
    "blender": (2, 93, 4),
    "category": "Object",
    "version": (1, 0),
    "category": "User Interface",
    "wiki_url": "https://github.com/RichardEllicott/GodotSnippets/",
    "support": "COMMUNITY"
}
"""

working on simple addon, Blender 2.9 grid double/half shortcuts


"""



import bpy
import bmesh
import sys
import inspect  # scans for classes, i have a macro script looking for classes beginning with "AUTO"
from mathutils import Matrix, Vector, Euler
import random
import math
from collections import defaultdict



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

def half_grid_scale():
    set_grid_scale(get_grid_scale() / 2.0)

def double_grid_scale():
    set_grid_scale(get_grid_scale() * 2.0)



"""
class AUTO_DDoubleGrid(bpy.types.Operator):
    """
    """
    bl_idname = "object.ddouble_grid"

    bl_label = "double grid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # origin_to_corner()

        bpy.ops.view3d.snap_all_selected_to_grid()

        return {'FINISHED'}
"""


class AUTO_ObjectDoubleGridScale(bpy.types.Operator):
    """Object Double Grid Scale"""
    # bl_idname = "object.double_grid_scale"
    bl_idname = "edit.double_grid_scale"

    bl_label = "Double Grid Scale"
    bl_options = {'REGISTER', 'UNDO'}

    screen_editing_hotkey = {
        # NUMPAD_PLUS RIGHT_BRACKET https://docs.blender.org/api/2.82/bpy.types.KeyMapItem.html#bpy.types.KeyMapItem.type
        "type": "RIGHT_BRACKET",
        "value": 'PRESS'
    }

    # PASTED
    # kmi = km.keymap_items.new(ObjectCursorArray.bl_idname, 'T', 'PRESS', ctrl=True, shift=True)
    # https://docs.blender.org/api/2.82/bpy.types.KeyMapItem.html#bpy.types.KeyMapItem

    # total: bpy.props.IntProperty(name="Steps", default=2, min=1, max=100) # was for the shortcut context

    def execute(self, context):
        double_grid_scale()
        # set_default_grid_settings() # REMOVED!!! 
        # feedback:
        # https://docs.blender.org/api/blender_python_api_2_75_release/bpy.types.Operator.html?highlight=report#bpy.types.Operator.report
        self.report({"INFO"}, "grid_scale = {}".format(get_grid_scale()))
        return {'FINISHED'}



class AUTO_ObjectHalfGridScale(bpy.types.Operator):
    """Object Half Grid Scale"""
    bl_idname = "edit.half_grid_scale"

    bl_label = "Half Grid Scale"
    bl_options = {'REGISTER', 'UNDO'}

    # pars listed here: https://docs.blender.org/api/2.82/bpy.types.KeyMapItems.html#bpy.types.KeyMapItems.new
    # https://docs.blender.org/api/2.82/bpy.types.KeyMapItem.html
    screen_editing_hotkey = {
        "type": "LEFT_BRACKET",  # NUMPAD_MINUS LEFT_BRACKET
        "value": 'PRESS'
    }

    def execute(self, context):
        # set_default_grid_settings()
        half_grid_scale()
        self.report({"INFO"}, "grid_scale = {}".format(get_grid_scale()))
        return {'FINISHED'}



# FOLLOWS OLD TUNNEL TOOLS BOILERPLATE, NO LONGER LOADS SHORTCUTS PROPERLY
# USES A REFLECTION PATTERN TO LOAD CLASSES
# SORRY BOILERPLATE OLD, LIKE MOST MY CODE, SIMPLE STILL WORK (this allows me to code with my terrible memory!)
# SO NOT YET REFACTORED SINCE 2.8
# CONFIRMED BOILERPLATE WORKS!

def menu_func(self, context):  # not used atm
    self.layout.operator(ObjectDoubleGridScale.bl_idname)


# store keymaps here to access after registration
addon_keymaps = []

register_list = []  # automatically add classes beginning with "AUTO" here, for auto register


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

        # kmi.properties.total = 0 # EXPERIMENTAL FOR 2.9 COMPAT

        for ob in register_list:
            if hasattr(ob, 'screen_editing_hotkey') and ob.screen_editing_hotkey:  # FIND OUR CUSTOM KEY SETUP DICTS

                pars_dict = {"idname": ob.bl_idname}  # building the pars dictionary to load into function
                pars_dict.update(ob.screen_editing_hotkey)
                kmi_A = screen_editing_keys.keymap_items.new(**pars_dict)  # ADD THE ACTUAL KEY (BECOMES LIVE HERE)
                addon_keymaps.append((screen_editing_keys, kmi_A))  # stored for later access (optional)

                # kmi.properties.total += 1 # EXPERIMENTAL FOR 2.9 COMPAT

            if hasattr(ob, 'object_mode_hotkey') and ob.object_mode_hotkey:

                pars_dict = {"idname": ob.bl_idname}
                pars_dict.update(ob.object_mode_hotkey)
                kmi_A = object_mode_keys.keymap_items.new(**pars_dict)
                addon_keymaps.append((object_mode_keys, kmi_A))

                # kmi.properties.total += 1 # EXPERIMENTAL FOR 2.9 COMPAT


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

    macro_keyword = "AUTO"

    # REFLECTION code, will automatically add any classes that begin with "AUTO"
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            if name.startswith(macro_keyword):
                if not obj in register_list:  # if not already in the register list
                    register_list.append(obj)  # add it

                    print("class automatically loaded: \"{}\"".format(obj, macro_keyword))

    register()




