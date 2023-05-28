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




I STLL CAN"T GET https://github.com/Muthird/CommandRecorder2.8 working!!!
need to try and fix bug
it looks like something i might want to add to this


Notes about my keymap i normally use

Preferences -> Keymap -> Blender27X profile
Preferences -> Keymap -> Remap all "View Selected" from "Numpad ." to "."   ----- Now "Frame Selected" to "." (not "Numpad .")
Preferences -> Input -> Keyboard -> check "Emulate Numpad" ("Emulate Numpad" now doesn't emulate "Numpad ." for the "." key )
3D View's "View" side panel > View > Clip (End) to 10'000


View Selected Issue in Blender 2.8, changed to "frame selected"
3D View -> Frame Selected set to just . (not numpad)



Preferences -> Input -> Addons:  (my choices)
    -Node: Node Wrangler
    -Import-Export: Import Images as Planes
    -Add Mesh: Extra Objects (adds rock generator, regular solids, gears)
    -Add Curve: Extra Objects
    -Mesh: Loop Tools (you can take squares from sub and make into circle)

    -Interface: Copy Attributes Menu (allows copying single modifier)



    -Object: Bool Tool

    -Node: Node Presets??? (allows to set a folder of node presets) (DID NOT WORK REPLACED WITH VX)
    -Material: Material Library (solves material issue)

    https://github.com/Lichtso/curve_cad
    Curve: Curve CAD Tools (may solve merging the paths vertices)
    THEN FOUND TO JUST DELETE, BUT CHECK THIS ANYWAY


    -Drop It Addon (https://gumroad.com/l/drop_it) (can drop trees and objects on ground)


TODO ADDON:
    make all vertices the same Y height, maybe based on the last selected
    can you snap them to grid together?


Football Pitch:

middle to top of goal line
105.0/2.0 - 16.5 pos
68.0/2.0 -



105.0/2.0 - 5.5 pos


FEATURE SUGGESTIONS

Snap object down to collider blender?



Moving to 2.9 Notes (CURRENTLY BROKEN!!)


To see the scripts i've added, i need to activate Preferences->Display->DeveloperExtras (as they don't have menu entries)

https://docs.blender.org/manual/en/latest/interface/controls/templates/operator_search.html#bpy-ops-wm-search-operator


The keyboard shortcuts have stopped working!



"""


import bpy
import bmesh
import sys
import inspect  # scans for classes, i have a macro script looking for classes beginning with "AUTO"
from mathutils import Matrix, Vector, Euler
import random
import math
from collections import defaultdict
import random

print(sys.version_info)
# sys.version_info(major=3, minor=4, micro=2, releaselevel='final', serial=0)
print(sys.version_info.major)
# 3


def print_classes():
    # https://stackoverflow.com/questions/1796180/how-can-i-get-a-list-of-all-classes-within-current-module-in-python
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            print(obj, " ++ ", name)


print("\n" * 4)

print("loading my_grid_double_shortcut_addon.blender2...")


# load Blender ICE Library...
# this is an experimental way of loading a library from an absolute path, it also forces a refresh so you can edit the library
# then reload this script in blender
# THIS CODE CAUSED WINDOWS CRASH DEACTIVATED

"""
libray_path = "/Users/rich/Documents/GitHub/myrepos/BlenderSnippets/experimental"


def add_library_search_path(path):
    if not path in sys.path:
        sys.path.append(path)


add_library_search_path(libray_path)

import blender_ice_library as ice

import importlib  # import internals
importlib.reload(ice)  # force reload of library
"""

# Preferences:
# TODO https://docs.blender.org/api/blender_python_api_2_68_release/bpy.types.AddonPreferences.html
# Preferences menu?


# Begin Plugin

# Functions:


def select_vertices_same_height():
    """
    to make all selected vertices same height
    https://www.blender.org/forum/viewtopic.php?t=18220

    in edit mode, select vertices, last one is height
    S 0-> Z -> 0 -> LMB

    scale -> Z only -> 0 scale -> LMB to finish


    IMPORTANT... this code is obsolete, highlight all vertices, scales them in one axis to 0, this will make them the same height
    """

    # just gets selected indexes as dicts of selected objects
    # https://blender.stackexchange.com/questions/1412/efficient-way-to-get-selected-vertices-via-python-without-iterating-over-the-en

    # # MORE ADVANCED SNIPPET AS IT GETS ALL OBJECTS IN EDIT MODE (SINCE 2.8 MULTI OBJECT EDIT MODe)
    dic_v = {}
    vertices = []
    for o in bpy.context.objects_in_mode:
        dic_v.update({o: []})
        bm = bmesh.from_edit_mesh(o.data)
        n = 0
        for v in bm.verts:
            if v.select:
                dic_v[o].append(v.index)
                vertices.append(v)

            n += 1
    print(dic_v)
    print(vertices)

    for v in vertices:
        # v.co.z = vertices[len(vertices)-1].co.z

        v.co.z = vertices[0].co.z

    # THE VIEW DOES NOT REFRESH, SO FLICK TO OBJECT AND BACK!
    # https://blender.stackexchange.com/questions/98863/update-edge-info-when-using-script-in-edit-mode
    bpy.ops.object.editmode_toggle()  # HACK
    bpy.ops.object.editmode_toggle()  # HACK

    # UNFORTUNATLY WE CANNOT SEEM TO WORK OUT THE LAST SELECTED VERTEX, SO MAYBE USE THE LOWEST ONE?


def get_vertex_positions():
    """
    https://blender.stackexchange.com/questions/1311/how-can-i-get-vertex-positions-from-a-mesh

    fucked
    """
    obj = bpy.context.active_object

    if obj.mode == 'EDIT':
        bm = bmesh.from_edit_mesh(obj.data)
        vertices = bm.verts

    else:
        vertices = obj.data.vertices

    verts = [obj.matrix_world * vert.co for vert in vertices]

    # coordinates as tuples
    plain_verts = [vert.to_tuple() for vert in verts]
    print(plain_verts)


class AUTO_ObjectVerticesSameHeight(bpy.types.Operator):
    """
    OBSOLETE, use a technique of scaling the vert positions on x y or z to 0
    """

    # bl_idname = "object.double_grid_scale"
    bl_idname = "edit.vertices_same_height"

    bl_label = "Vertices Same Height"
    bl_options = {'REGISTER', 'UNDO'}

    # screen_editing_hotkey = {
    #     # NUMPAD_PLUS RIGHT_BRACKET https://docs.blender.org/api/2.82/bpy.types.KeyMapItem.html#bpy.types.KeyMapItem.type
    #     "type": "NUMPAD_PLUS",
    #     "value": 'PRESS'
    # }

    # PASTED
    # kmi = km.keymap_items.new(ObjectCursorArray.bl_idname, 'T', 'PRESS', ctrl=True, shift=True)
    # https://docs.blender.org/api/2.82/bpy.types.KeyMapItem.html#bpy.types.KeyMapItem

    # total: bpy.props.IntProperty(name="Steps", default=2, min=1, max=100) # was for the shortcut context

    def execute(self, context):
        select_vertices_same_height()

        # double_grid_scale()
        # set_default_grid_settings()
        # # feedback:
        # # https://docs.blender.org/api/blender_python_api_2_75_release/bpy.types.Operator.html?highlight=report#bpy.types.Operator.report
        # self.report({"INFO"}, "grid_scale = {}".format(get_grid_scale()))
        return {'FINISHED'}


def origin_to_bottom(ob, matrix=Matrix()):
    """
    set the origin of an obhect to it's center at the bottom, like for a chess piece

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


def origin_to_corner(corner=0):  # on all selected
    """

    set all selected objects origin to the chosen "corner", default: left-back-bottom

    # https://blender.stackexchange.com/questions/141248/how-to-set-origin-points-of-multiple-objects-to-a-corner-of-their-bounding-boxes

    0 left back bottom 0,0,0
    1 left back top 0,0,1
    2 left forward top  0,1,1
    3 left forward bottom 0,1,0
    4 right back bottom 1,0,0
    5 right back top 1,0,1
    6 right forward top 1,1,1
    7 right forward bottom 1,1,0
    """

    context = bpy.context

    meshobs = defaultdict(list)
    for o in context.selected_objects:
        if o.type == 'MESH':
            meshobs[o.data].append(o)

    for me, obs in meshobs.items():
        o = obs[0]
        bbox = [Vector(b) for b in o.bound_box]
        # lhc = bbox[0] # ORGINAL left bottom
        lhc = bbox[corner]  # NEW
        T = Matrix.Translation(-lhc)
        me.transform(T)
        for o in obs:
            o.matrix_world.translation = o.matrix_world @ lhc


def origin_to_center():
    """
    for all the selected objects, make their origins go to the center of the bounding box
    """

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
    """
    WAS USED, BUT THEN FOUND ICON!
    """
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


def set_default_grid_settings():
    """
    automatically sets the scene units to none and the grid subdivisions to 8

    it's a bit of a hack to make my life easier, may be annoying
    """
    bpy.context.scene.unit_settings.system = 'NONE'
    set_grid_subdivisons(8)


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

    if not GEN_NAME in ob.modifiers:  # if we don't have one already create it
        ob.modifiers.new(GEN_NAME, type='UV_PROJECT')  # THIS STYLE DOESN'T CHANGE THE ACTIVE SELECTED OBJECT

    mod = ob.modifiers[GEN_NAME]  # POTENTIAL BUG: THIS MIGHT NOT HAVE THE RIGHT NAME

    mod.projector_count = len(PROJECTOR_NAMES)  # set camera count
    for (i, v) in enumerate(PROJECTOR_NAMES):
        mod.projectors[i].object = bpy.data.objects[v]  # set all the cameras
    mod.scale_x = SCALE
    mod.scale_y = SCALE
    mod.show_expanded = False


# PROCEDURAL GENERATION FUNCTIONS:

def remove_object(ob):
    bpy.data.objects.remove(ob, do_unlink=True)  # remove an object from scene (note, reload to fully clear memory)


def remove_scene_objects(key=None):
    """
    remove all objects beginning with a key (which marks the generated objects)
    """
    for ob in bpy.context.scene.objects:
        if key:
            if ob.name.startswith(key):
                bpy.data.objects.remove(ob, do_unlink=True)  # best option to delete, unlink first
        else:
            bpy.data.objects.remove(ob, do_unlink=True)  # best option to delete, unlink first


def select_all(): bpy.ops.object.select_all(action='SELECT')


def deselect_all(): bpy.ops.object.select_all(action='DESELECT')


def select_object(ob):  # https://devtalk.blender.org/t/selecting-an-object-in-2-8/4177
    ob.select_set(state=True)
    bpy.context.view_layer.objects.active = ob


def edit_mode():  # must have an object selected to enter this mode
    bpy.ops.object.mode_set(mode='EDIT')


def object_mode():
    bpy.ops.object.mode_set(mode='OBJECT')


def primitive_plane_add(**kwargs):  # reflection
    bpy.ops.mesh.primitive_plane_add(**kwargs)  # edit to new standards
    ob = bpy.context.active_object
    # ob.name = gen_key + ob.name  # set name
    ob.data.materials.append(default_material)  # add material
    created_objects.append(ob)
    return ob


def primitive_cube_add(**kwargs):
    bpy.ops.mesh.primitive_cube_add(**kwargs)  # edit to new standards
    ob = bpy.context.active_object
    # ob.name = gen_key + ob.name  # set name
    ob.data.materials.append(default_material)  # add material
    created_objects.append(ob)
    return ob


def point_cloud(ob_name, coords, edges=[], faces=[]):
    """
    Create point cloud object based on given coordinates and name.

    Keyword arguments:
    ob_name -- new object name
    coords -- float triplets eg: [(-1.0, 1.0, 0.0), (-1.0, -1.0, 0.0)]

    # https://blender.stackexchange.com/questions/23086/add-a-simple-vertex-via-python

    """

    # Create new mesh and a new object
    me = bpy.data.meshes.new(ob_name + "Mesh")
    ob = bpy.data.objects.new(ob_name, me)

    # Make a mesh from a list of vertices/edges/faces
    me.from_pydata(coords, edges, faces)

    # Display name and update the mesh
    ob.show_name = True
    me.update()

    # Link object to the active collection
    bpy.context.collection.objects.link(ob)

    return ob


def get_selected_verts():
    """
    returns a dictionary to handle the multi-object support
    https://blender.stackexchange.com/questions/1412/efficient-way-to-get-selected-vertices-via-python-without-iterating-over-the-en
    """
    dic_v = {}
    for o in bpy.context.objects_in_mode:
        dic_v.update({o: []})
        bm = bmesh.from_edit_mesh(o.data)
        for v in bm.verts:
            if v.select:
                dic_v[o].append(v.index)

    return dic_v


def select_vert(id):
    """
    bad looking hack selects a vert

    this very likely breaks if multiple objects are selected
    """

    bpy.ops.object.mode_set(mode='OBJECT')  # we need to exit out to object mode
    obj = bpy.context.active_object  # get the active object
    bpy.ops.object.mode_set(mode='EDIT')  # back to edit mode
    bpy.ops.mesh.select_mode(type="VERT")  # vert mode
    bpy.ops.mesh.select_all(action='DESELECT')  # ensure nothing else selected
    bpy.ops.object.mode_set(mode='OBJECT')  # back to object mode to select the vert!
    obj.data.vertices[id].select = True  # ensure selected vert
    bpy.ops.object.mode_set(mode='EDIT')  # back to edit mode!


def extrude_vert(translation=(0, 0, 1)):
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": translation})  # extrude selected vert


def my_tree_generator():

    gen_key = "MyTreeGenTreeA"  # IMPORTANT KEY FOR REFERENCE

    remove_scene_objects(gen_key)  # remove previous tree

    ob = point_cloud(gen_key, [(0.0, 0.0, 0.0)])

    select_object(ob)
    edit_mode()

    # bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 1)}) # extrude selected vert
    # bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 1)}) # extrude selected vert

    print("***SELECTED VERT DEBUG***")
    print(get_selected_verts())

    # select_vert(0)

    # bpy.ops.transform.skin_resize(value=(2.0, 2.0, 2.0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    # bpy.ops.transform.skin_resize(value=(2.0, 2.0, 2.0))

    # add the skin modifier
    modifier_name = "SKINGEN"
    ob.modifiers.new(modifier_name, type='SKIN')  # THIS STYLE DOESN'T CHANGE THE ACTIVE SELECTED OBJECT
    mod = ob.modifiers[modifier_name]  # POTENTIAL BUG: THIS MIGHT NOT HAVE THE RIGHT NAME

    # and sub
    modifier_name = "SUBDIV"
    ob.modifiers.new(modifier_name, type='SUBSURF')  # THIS STYLE DOESN'T CHANGE THE ACTIVE SELECTED OBJECT
    mod = ob.modifiers[modifier_name]  # POTENTIAL BUG: THIS MIGHT NOT HAVE THE RIGHT NAME
    mod.levels = 1
    mod.render_levels = 2
    mod.quality = 3

    object_mode()

    base_radius = 8.0

    # changing the vert skin radius (must be done in object mode)
    # https://blender.stackexchange.com/questions/1592/access-skin-modifier-radius-data
    ob.data.skin_vertices[0].data[0].radius = base_radius, base_radius  # makes the first radius 1.0

    node_list = [{'id': 0, 'depth': 1, 'direction': Vector((0.0, 0.0, 1.0))}]

    noise = 1.0 / 2.0

    max_branch_size = 6

    extrude_length = 16.0

    while len(node_list) > 0:

        data = node_list.pop()
        vert = data['id']
        depth = data['depth']
        direction = data['direction']

        direction = Vector(
            (direction.x + (random.uniform(-1.0, 1.0) * noise),
                direction.y + (random.uniform(-1.0, 1.0) * noise),
                direction.z + (random.uniform(-1.0, 1.0) * noise)))
        direction.normalize()  # normalize the vector

        # ALL VERTS GET THE RADIUS SET
        select_vert(vert)
        branch_radius = 1.0 / depth * base_radius
        object_mode()
        ob.data.skin_vertices[0].data[vert].radius = branch_radius, branch_radius
        edit_mode()

        if depth < max_branch_size:  # ONLY ADD NEW NODES SHOULD THEY NOT BE OVER MAX DEPTH

            select_vert(vert)  # ensure vert selected
            extrude_vert(direction * extrude_length)  # extrude up
            selected_verts = get_selected_verts()[bpy.data.objects[gen_key]]  # read new selected verts
            node_list.append({'id': selected_verts[0], 'depth': depth + 1, 'direction': direction})  # append it to the recursion list

        pass


class AUTO_MyTreeGenerator(bpy.types.Operator):
    """

    Object My Tree Generator


    starting with a manual way, maybe we should use bmesh?
    https://docs.blender.org/api/current/bmesh.html





    """
    # bl_idname = "object.double_grid_scale"
    bl_idname = "edit.my_tree_generator"

    bl_label = "My Tree Generator"
    bl_options = {'REGISTER', 'UNDO'}

    # total: bpy.props.IntProperty(name="Steps", default=2, min=1, max=100) # was for the shortcut context

    def execute(self, context):
        print("running my tree generator...")

        my_tree_generator()

        return {'FINISHED'}


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


class AUTO_ObjectOriginToBottom(bpy.types.Operator):
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


class AUTO_ObjectOriginToCorner(bpy.types.Operator):
    """
    """
    bl_idname = "object.object_origin_to_corner"

    bl_label = "Origin to Corner (left hand corner)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        origin_to_corner()
        return {'FINISHED'}


class AUTO_ObjectMoveToPosition(bpy.types.Operator):
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


class AUTO_ObjectOriginToCenter(bpy.types.Operator):
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


# class AUTO_ObjectTagCol(bpy.types.Operator):
#     """
#     ensure all selected objects end with the -col tag, allowing Godot to generate a static collider

#     ignore any objects that have the tag "<nocol>" in name


#     https://docs.godotengine.org/en/stable/getting_started/workflow/assets/importing_scenes.html?highlight=importing%20assets#godot-scene-importer


#     """
#     bl_idname = "object.object_tag_col"

#     bl_label = "Append Object Name -col"
#     bl_options = {'REGISTER', 'UNDO'}

#     def execute(self, context):
#         for ob in bpy.context.selected_objects:
#             if ob.type == 'MESH':  # only apply to mesh objects
#                 if not ob.name.endswith("-col"):  # if already tagged, just ignore

#                     ob.name = ob.name.replace("-col", "")  # clean out any other -col tags, sometimes causing issues

#                     if not "<nocol>" in ob.name:  # special ignore tag (nocol)
#                         ob.name = ob.name + "-col"  # -col appended to end so Godot will find it

#         return {'FINISHED'}


# class AUTO_ObjectRemoveTagCol(bpy.types.Operator):
#     """
#     opposite function designed to clear away the -col tags

#     """
#     bl_idname = "object.object_remove_tag_col"

#     bl_label = "Remove Object Name -col"
#     bl_options = {'REGISTER', 'UNDO'}

#     def execute(self, context):

#         for ob in bpy.context.selected_objects:
#             if ob.type == 'MESH':

#                 ob.name = ob.name.replace("-colonly", "")  # removes any existing "-colonly" sequences in name

#                 ob.name = ob.name.replace("-col", "")  # removes any existing "-col" sequences in name

#         return {'FINISHED'}


# class AUTO_ObjectTagExportAppend(bpy.types.Operator):
#     """

#     Uses my custom tagging system that overcomes issues when duplicating objects (with the numbers)


#     While working in blender I leave tags like <col> etc in the names

#     This script would convert "Cube<col>.004" => "Cube<col>.004-col"


#     """
#     bl_idname = "object.object_tag_export_append"

#     bl_label = "Append Object Name -col (based on existed <col> tags)"
#     bl_options = {'REGISTER', 'UNDO'}

#     def execute(self, context):
#         # origin_to_corner()

#         for o in bpy.context.selected_objects:
#             if o.type == 'MESH':

#                 # docs: https://docs.godotengine.org/en/stable/getting_started/workflow/assets/importing_scenes.html

#                 know_tags = [

#                     "col",  # standard collision (ensure model is simple enough for trimesh) (STATIC)

#                     "noimp",  # no import
#                     "convcol",  # convex polygon shape, can be faster but not recommended for level geometry (STATIC)
#                     "colonly",  # will create a static mesh but will be invisible (good for ramps under stairs etc) (STATIC) (can be used with empties)
#                     "convcolonly",  # as above with convex
#                     "navmesh",  # will remove mesh replace with navigation
#                     "vehicle",
#                     "wheel",
#                     "rigid",  # for making them movable crates

#                     "loop",  # these don't need a hyphen but we use one anyway
#                     "cycle"


#                 ]

#                 for tag in know_tags:
#                     if "<%s>" % tag in o.name:
#                         if not o.name.endswith("-" + tag):

#                             o.name = o.name + "-" + tag

#         return {'FINISHED'}


class AUTO_ObjectGodotExportTidy(bpy.types.Operator):
    """

    Godot Export Tidy

    go through all selected objects and check for tags like -col -rigid etc
    ensure they are at the back and not in the middle of the string:

    "Bear-col.002" => "Bear.002-col"

    also removes my old tags:

    "Bear<col>.005" => "Bear.005-col"



    is not always perfect as can sometimes find the object gets renamed


    """
    bl_idname = "object.object_tag_export_sort"

    bl_label = "Godot: sort out all godot export tags (-col etc to back)"
    bl_options = {'REGISTER', 'UNDO'}

    know_tags = [

        

        "noimp",  # no import
        
        "colonly",  # static trimesh, deletes the mesh leaves collider (can be used with empties)

        "col",  # static collision (ensure model is simple enough for trimesh), check AFTER colonly
        

        "convcolonly",  # convex static collider, then delete this mesh
        "convcol",  # convex static collider, can be faster but geometry must be convex


        "navmesh",  # will remove mesh replace with navigation
        "vehicle",
        "wheel",
        "rigid",  # for making them movable crates

        "loop",  # these don't need a hyphen but we use one anyway
        "cycle"

        

    ]

    # attempt to make function that will only rename if no conflict, return true or false

    def rename_object(self, o, new_name):

        orginal_name = o.name
        o.name = new_name

        if o.name == new_name:
            return True
        else:
            o.name = orginal_name
            return False

    # attempt to remove the .345.001.231 numbers that build up, works to reduce to just two at max

    def tidy_object_number(self, o):

        print("tidy name, ", o.name)

        orginal_name = o.name

        split = o.name.split('.')
        # if len(split) > 2:
        # o.name = split[0]

        digit_block_count = 0

        rebuild = []

        digit_blocks = []

        for block in split:
            if len(block) == 3 and block.isdigit():
                digit_block_count += 1

                digit_blocks.append(block)

            else:
                rebuild.append(block)  # only keep non digit block

        if digit_block_count > 1:

            # method 1
            # o.name = ".".join(rebuild) + "." + digit_blocks[-1] # try to keep old number

            # method 2 .... this method seems best, it always settles on two .726.273-col etc
            ran_string = "{}{}{}".format(str(random.randint(0, 9)), str(random.randint(0, 9)), str(random.randint(0, 9)))

            # ran_string += "."
            # for i in range(3):
            # ran_string += str(random.randint(0,9))

            o.name = ".".join(rebuild) + "." + ran_string

    def tidy_object_name(self, o):

        #self.tidy_object_number(o)

        for tag in self.know_tags:
            check_string = "-%s" % tag  # check for tag like -col

            tag_string = "<%s>" % tag

            if check_string in o.name:  # if tag in name
                if not o.name.endswith(check_string):  # tag not already at end

                    o.name = o.name.replace(check_string, "") + check_string  # new name remove he old name, add tag to end
                    break
                    # note at this point blender could end up renaming due to duplicates, add .001 after our tag!

                elif tag_string in name:  # replaces the old tags
                    o.name = o.name.replace(tag_string, "") + check_string
                    break

                # split = o.name.split('.')
                # if len(split) > 2:

                #     pass

                break

    def execute(self, context):
        # origin_to_corner()

        for o in bpy.context.selected_objects:
            if o.type == 'MESH':

                # docs: https://docs.godotengine.org/en/stable/getting_started/workflow/assets/importing_scenes.html

                self.tidy_object_name(o)

                # for tag in self.know_tags:
                #     check_string = "-%s" % tag  # check for tag like -col

                #     tag_string = "<%s>" % tag

                #     if check_string in o.name:  # if tag in name
                #         if not o.name.endswith(check_string):  # tag not already at end
                #             o.name = o.name.replace(check_string, "") + check_string  # new name remove he old name, add tag to end

                #             # note at this point blender could end up renaming due to duplicates, add .001 after our tag!

        return {'FINISHED'}


# class AUTO_ObjectPrepareForGodotExport(bpy.types.Operator):
#     """
#     """
#     bl_idname = "object.prepare_for_godot_export"

#     bl_label = "Prepare for Godot export"
#     bl_options = {'REGISTER', 'UNDO'}

#     def execute(self, context):
#         print("running script: AUTO_ObjectPrepareForGodotExport ...")


#         AUTO_ObjectTagExportAppend.execute(self,context) # run our script


#         return {'FINISHED'}


class AUTO_ObjectCopyUVProjectModifier(bpy.types.Operator):
    """
    testing adding modifiers etc

    ['DATA_TRANSFER', 'MESH_CACHE', 'MESH_SEQUENCE_CACHE', 'NORMAL_EDIT', 'WEIGHTED_NORMAL', 'UV_PROJECT', 'UV_WARP', 'VERTEX_WEIGHT_EDIT', 'VERTEX_WEIGHT_MIX', 'VERTEX_WEIGHT_PROXIMITY', 'ARRAY', 'BEVEL', 'BOOLEAN', 'BUILD', 'DECIMATE', 'EDGE_SPLIT', 'MASK', 'MIRROR', 'MULTIRES', 'REMESH', 'SCREW', 'SKIN', 'SOLIDIFY', 'SUBSURF', 'TRIANGULATE', 'WIREFRAME',
        'WELD', 'ARMATURE', 'CAST', 'CURVE', 'DISPLACE', 'HOOK', 'LAPLACIANDEFORM', 'LATTICE', 'MESH_DEFORM', 'SHRINKWRAP', 'SIMPLE_DEFORM', 'SMOOTH', 'CORRECTIVE_SMOOTH', 'LAPLACIANSMOOTH', 'SURFACE_DEFORM', 'WARP', 'WAVE', 'CLOTH', 'COLLISION', 'DYNAMIC_PAINT', 'EXPLODE', 'OCEAN', 'PARTICLE_INSTANCE', 'PARTICLE_SYSTEM', 'FLUID', 'SOFT_BODY', 'SURFACE']


    """
    bl_idname = "object.copy_uv_project_modifier"

    bl_label = "Add UV Project Modifier (with default uv projector links)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("running script: AUTO_ObjectCopyUVProjectModifier ...")

        for ob in bpy.context.selected_objects:
            if ob.type == 'MESH':
                add_custom_uv_to_ob(ob)

        return {'FINISHED'}


class AUTO_ObjectTestScriptA(bpy.types.Operator):
    """
    testing adding modifiers etc

    ['DATA_TRANSFER', 'MESH_CACHE', 'MESH_SEQUENCE_CACHE', 'NORMAL_EDIT', 'WEIGHTED_NORMAL', 'UV_PROJECT', 'UV_WARP', 'VERTEX_WEIGHT_EDIT', 'VERTEX_WEIGHT_MIX', 'VERTEX_WEIGHT_PROXIMITY', 'ARRAY', 'BEVEL', 'BOOLEAN', 'BUILD', 'DECIMATE', 'EDGE_SPLIT', 'MASK', 'MIRROR', 'MULTIRES', 'REMESH', 'SCREW', 'SKIN', 'SOLIDIFY', 'SUBSURF', 'TRIANGULATE', 'WIREFRAME',
        'WELD', 'ARMATURE', 'CAST', 'CURVE', 'DISPLACE', 'HOOK', 'LAPLACIANDEFORM', 'LATTICE', 'MESH_DEFORM', 'SHRINKWRAP', 'SIMPLE_DEFORM', 'SMOOTH', 'CORRECTIVE_SMOOTH', 'LAPLACIANSMOOTH', 'SURFACE_DEFORM', 'WARP', 'WAVE', 'CLOTH', 'COLLISION', 'DYNAMIC_PAINT', 'EXPLODE', 'OCEAN', 'PARTICLE_INSTANCE', 'PARTICLE_SYSTEM', 'FLUID', 'SOFT_BODY', 'SURFACE']


    """
    bl_idname = "object.test_script_a"

    bl_label = "Test Script A"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("running script: AUTO_ObjectTestScriptA ...")

        return {'FINISHED'}


class AUTO_SnapAllSelectedToGrid(bpy.types.Operator):
    """
    """
    bl_idname = "object.snap_all_selected_to_grid"

    bl_label = "Snap All Selected To Grid (cust script)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # origin_to_corner()

        bpy.ops.view3d.snap_all_selected_to_grid()

        return {'FINISHED'}


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
