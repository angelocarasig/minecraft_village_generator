import Foundation
import Fountain
from Floors import path_builder
from mcpi import minecraft, block
import threading

mc = minecraft.Minecraft.create()

x, y, z = mc.player.getPos()

x, y, z = Foundation.buildFoundation(x,y,z)

Fountain.build_fountain(x, y, z)

z -= 5

#CENTER POSITION:
x_main = x
y_main = y
z_main = z

#BUILD ROADS:

z -= 4
thread_north = threading.Thread(target=path_builder, args=(x, y, z, "North",))
thread_north.start()
z = z_main

x += 4
thread_east = threading.Thread(target=path_builder, args=(x, y, z, "East",))
thread_east.start()
x = x_main

z += 4
thread_south = threading.Thread(target=path_builder, args=(x, y, z, "South",))
thread_south.start()
z = z_main

x -= 4
thread_west = threading.Thread(target=path_builder, args=(x, y, z, "West",))
thread_west.start()
x = x_main