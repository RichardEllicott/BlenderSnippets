Example of importing a custom library in Blender's python


The normal way to do this is to make a library file like in normal python, however it will not load from the local folder the same way it would in python. Also loading the library while blender is still running leaves it loaded.

Instead of rebooting Blender, this template shows loading from a custom folder, and forcing a reload.


The libray_path must be the absolute path of the library