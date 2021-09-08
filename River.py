from mcpi import minecraft
import random
import math

mc = minecraft.Minecraft.create()

width = 3
x, y, z = mc.player.getPos()

mc.setBlocks(x,y-4,z,x,y+4,z+30,0)
mc.setBlocks(x,y-4,z,x,y-1,z+30,9)