from mcpi import block, entity, minecraft

mc = minecraft.Minecraft.create()

x, y, z = mc.player.getPos()

x = x+10
baseSize = 5
baseMat = block.STONE_BRICK
wallHeight = 4
wallMat = block.BRICK_BLOCK
mc.setBlocks(x+baseSize,y,z+baseSize,x-baseSize,y,z-baseSize,baseMat)   #Base gen

mc.setBlocks(x+baseSize,y+1,z+baseSize,x-baseSize,y+wallHeight,z-baseSize,wallMat)  #makes big cube for wall
mc.setBlocks(x+baseSize-1,y+1,z+baseSize-1,x-(baseSize-1),y+wallHeight,z-(baseSize-1),0)    #cuts out hole for the big cube
mc.setBlock(x-baseSize,y+1,z,block.AIR)
mc.setBlock(x-baseSize,y+2,z,block.AIR)
mc.setBlock(x-baseSize,y+1,z,64,0)
mc.setBlock(x-baseSize,y+2,z,64,8)