"""

Blender ICE Library v1.0 experimental

coded by Richard Ellicott



Designed to be my common library and make tasks easier

-like making objects in a more object-orientated way (passing object references back etc)


LOAD FROM ADDONS FOLDER:

import blender_ice_library as ice


LOAD FROM CUSTOM FOLDER:

def add_library_search_path(path):
    if not path in sys.path:
        sys.path.append(path)
add_library_search_path("/Users/rich/Documents/GitHub/myrepos/BlenderSnippets/experimental")

import blender_ice_library as ice # loads the library
import importlib # import internals
importlib.reload(ice) # force reload # forces a refresh, in-case of editing this library




"""
import bpy
import numpy

print("loading Blender ICE Library v1.0 experimental...")


class UI:

    _screen_area = None

    @property
    def screen_area(self):
        """
        reliable hack to get the VIEW_3D area object, allowing changing grid size

        get_area_object().overlay.grid_scale = 2
        get_area_object().overlay.grid_subdivisions = 8

        https://blender.stackexchange.com/questions/154610/how-do-you-programatically-set-grid-scale

        """
        if not self._screen_area:
            AREA = 'VIEW_3D'
            for window in bpy.context.window_manager.windows:
                for area in window.screen.areas:
                    if not area.type == AREA:
                        continue
                    for s in area.spaces:
                        if s.type == AREA:
                            self._screen_area = s
                            break

        return self._screen_area

    @property
    def grid_scale(self):
        return self.screen_area.overlay.grid_scale

    @grid_scale.setter
    def grid_scale(self, grid_scale):
        self.screen_area.overlay.grid_scale = grid_scale

    @property
    def grid_subdivisons(self):
        return self.screen_area.overlay.grid_subdivisions

    @grid_subdivisons.setter
    def grid_subdivisons(self, grid_subdivisions):
        self.screen_area.overlay.grid_subdivisions = grid_subdivisions

    def half_grid_scale(self):
        self.grid_scale = self.grid_scale / 2.0

    def double_grid_scale(self):
        self.grid_scale = self.grid_scale * 2.0


ui = UI()


class Math:

    def get_random_normal_vector(self, spread=1.0):
        return (numpy.random.normal(0.0, spread), numpy.random.normal(0.0, spread), numpy.random.normal(0.0, spread))



math = Math()


class ICE():

    def metaball_add(self,**kwargs):  # reflection
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

ice = ICE()


if __name__ == "__main__":
    print("blender_ice_library.py...")
