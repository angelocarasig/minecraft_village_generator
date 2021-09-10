from mcpi import block, minecraft, entity
import random
mc = minecraft.Minecraft.create()

x, y, z = mc.player.getPos()

#TODO: Add stairs and outdoor section
def genFirePit(x,y,z,mat):
    mc.setBlocks(x-1,y,z-1,x-1,y,z+1,mat,0)
    mc.setBlocks(x+1,y,z-1,x+1,y,z+1,mat,1)
    mc.setBlock(x,y,z-1,mat,2)
    mc.setBlock(x,y,z+1,mat,3)
    mc.setBlock(x,y-1,z,block.PUMPKIN)
    mc.setBlock(x,y,z,block.FIRE)
genFirePit(x,y,z,109)