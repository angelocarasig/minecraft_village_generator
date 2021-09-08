from mcpi import entity, minecraft
import random
import math

mc = minecraft.Minecraft.create()
x, y, z = mc.player.getPos()
mc.setBlock(x, y, z, 64, 0)
mc.setBlock(x, y+1, z, 64, 8)
#while True:
#    x, y, z = mc.player.getPos()
#    mc.spawnEntity(x,y,z,entity.PRIMED_TNT)



