"""


this solution allows loading the library from a custom folder, very useful for developing a script as the library will reload

https://blender.stackexchange.com/questions/51044/how-to-import-a-blender-python-script-in-another


for example, now this script, just pasted in, would search for the library in the correct path


"""


import bpy
import sys
import os

libray_path = "/Users/rich/Documents/GitHub/myrepos/BlenderSnippets/loading_a_library_dev_template" # set path to library location


if not libray_path in sys.path:
    print('append the path: {}'.format(libray_path))
    sys.path.append(libray_path)
else:
    print("path already in search paths: {}".format(libray_path))


print("sys.path: {}".format(sys.path))

import lib_test


# this next part forces a reload in case you edit the source after you first start the blender session
import imp # import internals
imp.reload(lib_test)

# this is optional and allows you to call the functions without specifying the package name
from lib_test import *

