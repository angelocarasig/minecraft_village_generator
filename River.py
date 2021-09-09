from mcpi import entity, minecraft
import random
import math

mc = minecraft.Minecraft.create()
x, y, z = mc.player.getPos() 
while True:
    x, y, z = mc.player.getPos()
    mc.spawnEntity(x,y,z,entity.VILLAGER)



