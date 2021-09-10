from mcpi.minecraft import Minecraft
from mcpi import block
from time import sleep
import random
import threading

mc = Minecraft.create()

def get_compass_direction():
    angle = mc.player.getRotation()
    mc.postToChat("Angle:")
    mc.postToChat(angle)
    if 90 + 45 < angle <= 180 + 45:
        return "North"
    if 180 + 45 < angle <= 270 + 45:
        return "East"
    if 270 + 45 < angle <= 360 or angle <= 45:
        return "South"
    if 0 + 45 < angle <= 90 + 45:
        return "West"

current_direction = get_compass_direction()

#Looks like just float vals
def build_fountain(x, y, z, block_type = block.DIAMOND_BLOCK, light_type = block.GLOWSTONE_BLOCK, path = block.GRASS):
    
    #Path
    x, y, z = x, y-1, z-5

    mc.setBlocks(x, y, z, x, y + 3, z, light_type)

    #NESW
    t1 = threading.Thread(mc.setBlocks(x + 1, y+1, z - 3, x - 1, y + 1, z - 3, block_type))
    t2 = threading.Thread(mc.setBlocks(x + 1, y+1, z + 3, x - 1, y + 1, z + 3, block_type))
    t3 = threading.Thread(mc.setBlocks(x + 3, y+1, z - 1, x + 3, y + 1, z + 1, block_type))
    t4 = threading.Thread(mc.setBlocks(x - 3, y+1, z - 1, x - 3, y + 1, z + 1, block_type))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    #Corners
    t5 = mc.setBlock(x+ 2, y + 1, z + 2, block_type)
    t6 = mc.setBlock(x- 2, y + 1, z + 2, block_type)
    t7 = mc.setBlock(x+ 2, y + 1, z - 2, block_type)
    t8 = mc.setBlock(x- 2, y + 1, z - 2, block_type)

    mc.setBlock(x, y+4, z, block.WATER)

    mc.setBlocks(x-3, y, z+1, x+3, y, z-1, block.STONE_BRICK)
    mc.setBlocks(x-1, y, z+3, x+1, y, z-3, block.STONE_BRICK)

    mc.setBlock(x+ 2, y, z + 2, block.STONE_BRICK)
    mc.setBlock(x- 2, y, z + 2, block.STONE_BRICK)
    mc.setBlock(x+ 2, y, z - 2, block.STONE_BRICK)
    mc.setBlock(x- 2, y, z - 2, block.STONE_BRICK)


    

# build_fountain(block_type = block.MOSS_STONE)

# #Middle of town should be center of fountain:
# x, y, z = mc.player.getPos()
# z = z - 5