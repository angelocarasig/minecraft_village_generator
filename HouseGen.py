from mcpi import block, minecraft
import random
mc = minecraft.Minecraft.create()

x, y, z = mc.player.getPos()

#TODO: Add stairs and outdoor section

x = x+10    #so the house spawn 10 x units infront of player
baseSize = random.randint(3,6)  #randomises base size
baseMatArr = [1,98,112,206,4,35,42,41,99,100,121,155,159,168,173,201,202,206]   #all the possible base materials
baseMat = random.choice(baseMatArr) #choses a random base mat
wallHeight = random.randint(3,5)    #randomises wall height
wallMatArr = [1,5,17,45,100,121,133,155,159,162,168,201,202,206]    #all the possible wall materials
wallMat = random.choice(wallMatArr) #choses a random wall mat
while wallMat == baseMat:   #makes sure that wall mat is not the same as base mat
    wallMat = random.choice(wallMatArr)
roofHeight = random.randint(2,baseSize+1)   #randomises how high the roof will go
roofMatArr = [5,19,20,22,1,98,112,206,4,35,42,41,99,100,121,155,159,168,173,201,202,206,2]  #all possible roof materials 
roofMat = random.choice(roofMatArr) #Chooses a random roof mat
while roofMat == baseMat or roofMat == wallMat: #makes sure it does not match the wall or floor
    roofMat = random.choice(wallMatArr)
lightMatArr = [89,50,169,91]    #all possible lighting blocks 
lightMat = random.choice(lightMatArr)   #chooses a lighting block
stairMatArr = [53,67,108,109,114,128,134,135,136,156,163,164,180,203]
stairMat = random.choice(stairMatArr)

def genHouse(x, y, z, baseSize, wallHeight, roofHeight, init = False):
    mc.setBlocks(x+baseSize,y,z+baseSize,x-baseSize,y,z-baseSize,baseMat)   #Makes base of the house section
    mc.setBlocks(x+baseSize,y+1,z+baseSize,x-baseSize,y+wallHeight,z-baseSize,wallMat)  #makes big cube for wall
    mc.setBlocks(x+baseSize-1,y+1,z+baseSize-1,x-(baseSize-1),y+wallHeight,z-(baseSize-1),0)    #cuts out hole for the big cube
    if init:
        stories = random.randint(2,2)   #randomises the amount of stories
    if init and stories != 1:   #makes the first roof flat if there are multiple stories
        mc.setBlocks(x+(baseSize),y+wallHeight+1,z+(baseSize),x-(baseSize),y+wallHeight+1,z-(baseSize),roofMat)
        if roofHeight != 0:
            mc.setBlocks(x+(baseSize-1),y+wallHeight+2,z+(baseSize-1),x-(baseSize-1),y+wallHeight+2,z-(baseSize-1),roofMat)
            mc.setBlocks(x+(baseSize-1),y+wallHeight+1,z+(baseSize-1),x-(baseSize-1),y+wallHeight+1,z-(baseSize-1),0)
    else:   #generates the roof
        for i in range(0,roofHeight):
            mc.setBlocks(x+(baseSize-i),y+wallHeight+1+i,z+(baseSize-i),x-(baseSize-i),y+wallHeight+1+i,z-(baseSize-i),roofMat) #Makes a big roof big slate
            if i != roofHeight-1:   #checks that it is not the last one
                mc.setBlocks(x+(baseSize-i-1),y+wallHeight+1+i,z+(baseSize-i-1),x-(baseSize-i-1),y+wallHeight+1+i,z-(baseSize-i-1),0)   #removes the insides of the roof
    #Generates lighting
    mc.setBlock(x+baseSize-1,y+wallHeight+1,z+baseSize-1,lightMat)
    mc.setBlock(x-baseSize+1,y+wallHeight+1,z+baseSize-1,lightMat)
    mc.setBlock(x+baseSize-1,y+wallHeight+1,z-baseSize+1,lightMat)
    mc.setBlock(x-baseSize+1,y+wallHeight+1,z-baseSize+1,lightMat)
    #Generates lighting
    
    if init:    #If it is running first
        doorHeight = random.randint(0,wallHeight-3) #randomising the interior door height
        #mc.setBlocks(x-baseSize,y+1,z,x-baseSize,y+2,z,block.AIR) #making door hole 
        mc.setBlock(x-baseSize, y+2, z, 64, 12)
        mc.setBlock(x-baseSize, y+1, z, 64, 1)
        genHouse(x,y,z+(baseSize*2),baseSize,wallHeight, roofHeight)
        mc.setBlocks(x+int(baseSize/2),y+1,z+baseSize,x-int(baseSize/2),y+2+doorHeight,z+baseSize,block.AIR) #making door hole for right room
        genHouse(x+(baseSize*2), y, z, baseSize, wallHeight, roofHeight)
        mc.setBlocks(x+baseSize,y+1,z+int(baseSize/2),x+baseSize,y+2+doorHeight,z-int(baseSize/2),block.AIR) #making door hole for back room
        genHouse(x+(baseSize*2),y,z+(baseSize*2),baseSize,wallHeight, roofHeight)
        mc.setBlocks(x+(baseSize*2)+int(baseSize/2),y+1,z+baseSize,x+(baseSize*2)-int(baseSize/2),y+2+doorHeight,z+baseSize,block.AIR) #making door hole for back right room
        mc.setBlocks(x+baseSize,y+1,z+(baseSize*2)+int(baseSize/2),x+baseSize,y+2+doorHeight,z+(baseSize*2)-int(baseSize/2),block.AIR) #making door hole for back right room

        oldY = y
        for i in range(1,stories):  #generates second story
            if roofHeight == 1: #Makes it generate one lower if the roof it too low
                y = y+wallHeight+1
            else:
                y = y+wallHeight+2  #increasing height so it can make second floor
            mc.setBlocks(x-baseSize,y+1,z,x-baseSize,y+2,z,block.AIR) #making door hole 
            genHouse(x,y,z+(baseSize*2),baseSize,wallHeight, roofHeight)
            mc.setBlocks(x+int(baseSize/2),y+1,z+baseSize,x-int(baseSize/2),y+2+doorHeight,z+baseSize,block.AIR) #making door hole for right room
            genHouse(x+(baseSize*2),y,z,baseSize,wallHeight, roofHeight)
            mc.setBlocks(x+baseSize,y+1,z+int(baseSize/2),x+baseSize,y+2+doorHeight,z-int(baseSize/2),block.AIR) #making door hole for back room
            genHouse(x+(baseSize*2),y,z+(baseSize*2),baseSize,wallHeight, roofHeight)
            mc.setBlocks(x+(baseSize*2)+int(baseSize/2),y+1,z+baseSize,x+(baseSize*2)-int(baseSize/2),y+2+doorHeight,z+baseSize,block.AIR) #making door hole back right room
            mc.setBlocks(x+baseSize,y+1,z+(baseSize*2)+int(baseSize/2),x+baseSize,y+2+doorHeight,z+(baseSize*2)-int(baseSize/2),block.AIR) #making door hole back right room
            mc.setBlocks(x+(baseSize*2)-1,oldY+wallHeight,z+baseSize+wallHeight-1,x+(baseSize*2)+1,oldY+wallHeight+2,(z+baseSize+wallHeight-1)-(wallHeight+1),block.AIR) #making hole for stairs
            genStairs(x+(baseSize*2),oldY+1,z+baseSize+wallHeight-1,height=wallHeight+2,width=1,facing='north',mat=stairMat)


def genStairs(x,y,z,height,width = 2,facing = 'east',mat = 1):
    if facing == 'south':
        for i in range(0,height):
            mc.setBlocks(x-width,y+i,z+i,x+width,y+i,z+i,mat,2)
    elif facing == 'east':
        for i in range(0,height):
            mc.setBlocks(x+i,y+i,z-width,x+i,y+i,z+width,mat,0)
    elif facing == 'west':
        for i in range(0,height):
            mc.setBlocks(x-i,y+i,z-width,x-i,y+i,z+width,mat,1)
    elif facing == 'north':
        for i in range(0,height):
            mc.setBlocks(x-width,y+i,z-i,x+width,y+i,z-i,mat,3)
    else:
        print('invalid direction')
    mc.setBlocks


genHouse(x+5,y,z,baseSize,wallHeight, roofHeight,True)