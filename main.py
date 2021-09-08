import Fountain
import Floors
from mcpi import minecraft, block

mc = minecraft.Minecraft.create()

x, y, z = mc.player.getPos()
Fountain.build_fountain()
z -= 5

#CENTER POSITION:
x_main = x
y_main = y
z_main = z

#BUILD ROADS:

#North
z -= 4
Floors.path_builder(x, y, z, "North")
z = z_main

#East
x += 4
Floors.path_builder(x, y, z, "East")
x = x_main

#South
z += 4
Floors.path_builder(x, y, z, "South")
z = z_main

#West
x -= 4
Floors.path_builder(x, y, z, "West")
x = x_main