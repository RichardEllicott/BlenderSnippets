"""

Calculator scratch sheet for geometry and ratios

"""
from math import * # import math functions to top level



# Circumradius and inradius (of regular octagon)
# https://en.wikipedia.org/wiki/Octagon#Circumradius_and_inradius


a = 1.0 # length of side

R = (sqrt(4.0 + 2.0 * sqrt(2.0)) / 2.0)  * a # circumradius
print("R = %s" % R)

r = ((1.0 + sqrt(2.0)) / 2.0) * a # inradius
print("r = %s" % r)


# in blender, create a circle with 8 sides, rotate it by 22.5 degrees, scale it by R/r (1.082392200292394)
oct_scale = R/r
print("oct_scale = %s" % oct_scale)



a = 1.0/(sqrt(4.0 + 2.0 * sqrt(2.0)) / 2.0)
print(a)




# Pythagoras

print("Diagonal Ratio for Square: %s" % (sqrt(2.0)))


print("TwoSquaresDiagonalRatio: %s" % (sqrt(pow(1.0,2.0)+pow(2.0,2.0))))














