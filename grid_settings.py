"""

editing the UI's grid scale

"""


import bpy


def get_3D_area_object():
    """
    reliable hack to get the VIEW_3D area object, allowing changing grid size

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
    set_grid_scale(get_grid_scale() / 2.0)


def double_grid_scale():
    set_grid_scale(get_grid_scale() * 2.0)


    
