from mcpi import block, minecraft
import random
mc = minecraft.Minecraft.create()

x, y, z = mc.player.getPos()



stories = random.randint(1,4)   #randomises the amount of stories
stairDir = random.randint(0,1)  #randomises the direction of the stairs
baseSize = random.randint(3,5)  #randomises base size   3,5
baseMatArr = [1,98,112,206,4,35,42,41,99,100,121,155,159,168,173,201,202,206]   #all the possible base materials
baseMat = random.choice(baseMatArr) #choses a random base mat
if baseSize == 3 and stories != 1:
    wallHeight = 3
else:
    wallHeight = random.randint(3,5)    #randomises wall height 3,5
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
doorHeight = random.randint(0,wallHeight-3) #randomising the interior door height

def genHouse(x, y, z, baseSize, wallHeight, roofHeight, init = False, dir = 'west'):
    mc.setBlocks(x+baseSize,y,z+baseSize,x-baseSize,y,z-baseSize,baseMat)   #Makes base of the house section
    mc.setBlocks(x+baseSize,y+1,z+baseSize,x-baseSize,y+wallHeight,z-baseSize,wallMat)  #makes big cube for wall
    mc.setBlocks(x+baseSize-1,y+1,z+baseSize-1,x-(baseSize-1),y+wallHeight,z-(baseSize-1),0)    #cuts out hole for the big cube
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
    mc.setBlock(x+baseSize-1,y+wallHeight+1,z+baseSize-1,lightMat,2)
    mc.setBlock(x-baseSize+1,y+wallHeight+1,z+baseSize-1,lightMat)
    mc.setBlock(x+baseSize-1,y+wallHeight+1,z-baseSize+1,lightMat,2)
    mc.setBlock(x-baseSize+1,y+wallHeight+1,z-baseSize+1,lightMat)
    #Generates lighting
    if init:    #If it is running first
        
        if(stories != 1):
            genFirePit(x,y+wallHeight+3,z,109)  #Makes fire pit
        if(dir == 'west'):
            mc.setBlock(x-baseSize, y+2, z, 64, 11) #Placing door
            mc.setBlock(x-baseSize, y+1, z, 64, 0)  #Placing door
            mc.setBlock(x-baseSize, y+2, z+2, block.STAINED_GLASS) #Placing window
            mc.setBlock(x-baseSize, y+2, z-2, block.STAINED_GLASS) #Placing window
            mc.setBlocks(x+int(baseSize/2),y+2,z-baseSize,x-int(baseSize/2),y+wallHeight-1,z-baseSize,block.STAINED_GLASS)  #making window
            #Generating other rooms
            genOtherRooms(x,y,z,doorHeight,houseFacing='west')
            tempY = y
            for i in range(1,stories):  #generates second story
                tempY = tempY + wallHeight + 2
                genOtherRooms(x,tempY,z,doorHeight,houseFacing='west')
                stairRoom = [x+(baseSize*2),z+(baseSize*2)]
                if stairDir == 1:
                    genStairs(stairRoom[0],tempY-wallHeight-1,stairRoom[1],height=wallHeight+2,width=1,facing='north',mat=stairMat)
                else:
                    genStairs(stairRoom[0],tempY-wallHeight-1,stairRoom[1],height=wallHeight+2,width=1,facing='west',mat=stairMat)
        elif(dir == 'east'):
            mc.setBlock(x+baseSize, y+2, z, 64, 13) #Placing door
            mc.setBlock(x+baseSize, y+1, z, 64, 2)  #Placing door
            mc.setBlock(x+baseSize, y+2, z-2, block.STAINED_GLASS) #Placing window
            mc.setBlock(x+baseSize, y+2, z+2, block.STAINED_GLASS)  #Placing window
            mc.setBlocks(x+int(baseSize/2),y+2,z+baseSize,x-int(baseSize/2),y+wallHeight-1,z+baseSize,block.STAINED_GLASS)  #making window
            #Generating other rooms
            genOtherRooms(x,y,z,doorHeight,houseFacing='east')
            tempY = y
            for i in range(1,stories):  #generates second story
                tempY = tempY + wallHeight + 2
                genOtherRooms(x,tempY,z,doorHeight,houseFacing='east')
                stairRoom = [x-(baseSize*2),z-(baseSize*2)]
                if stairDir == 1:
                    genStairs(stairRoom[0],tempY-wallHeight-1,stairRoom[1],height=wallHeight+2,width=1,facing='south',mat=stairMat)
                else:
                    genStairs(stairRoom[0],tempY-wallHeight-1,stairRoom[1],height=wallHeight+2,width=1,facing='east',mat=stairMat)         
        elif(dir == 'north'):
            mc.setBlock(x, y+2, z-baseSize, 64, 12) #Placing door
            mc.setBlock(x, y+1, z-baseSize, 64, 1)  #Placing door
            mc.setBlock(x+2, y+2, z-baseSize, block.STAINED_GLASS) #Placing window
            mc.setBlock(x-2, y+2, z-baseSize, block.STAINED_GLASS)  #Placing window
            mc.setBlocks(x+baseSize ,y+2,z-int(baseSize/2),x+baseSize,y+wallHeight-1,z+int(baseSize/2),block.STAINED_GLASS)  #making window
            #Generating other rooms
            genOtherRooms(x,y,z,doorHeight,houseFacing='north')
            tempY = y
            for i in range(1,stories):  #generates second story
                tempY = tempY + wallHeight + 2
                genOtherRooms(x,tempY,z,doorHeight,houseFacing='north')
                stairRoom = [x-(baseSize*2),z+ (baseSize*2)]
                if stairDir == 1:
                    genStairs(stairRoom[0],tempY-wallHeight-1,stairRoom[1],height=wallHeight+2,width=1,facing='north',mat=stairMat)
                else:
                    genStairs(stairRoom[0],tempY-wallHeight-1,stairRoom[1],height=wallHeight+2,width=1,facing='east',mat=stairMat)       
        elif(dir == 'south'):
            mc.setBlock(x, y+2, z+baseSize, 64, 14) #Placing door
            mc.setBlock(x, y+1, z+baseSize, 64, 3)  #Placing door
            mc.setBlock(x+2, y+2, z+baseSize, block.STAINED_GLASS) #Placing window
            mc.setBlock(x-2, y+2, z+baseSize, block.STAINED_GLASS)  #Placing window
            mc.setBlocks(x-baseSize ,y+2,z-int(baseSize/2),x-baseSize,y+wallHeight-1,z+int(baseSize/2),block.STAINED_GLASS)  #making window
            #Generating other rooms
            genOtherRooms(x,y,z,doorHeight,houseFacing='south')
            tempY = y
            for i in range(1,stories):  #generates second story
                tempY = tempY + wallHeight + 2
                genOtherRooms(x,tempY,z,doorHeight,houseFacing='south')
                stairRoom = [x+(baseSize*2),z-(baseSize*2)]
                if stairDir == 1:
                    genStairs(stairRoom[0],tempY-wallHeight-1,stairRoom[1],height=wallHeight+2,width=1,facing='south',mat=stairMat)
                else:
                    genStairs(stairRoom[0],tempY-wallHeight-1,stairRoom[1],height=wallHeight+2,width=1,facing='west',mat=stairMat)

def genOtherRooms(x,y,z,doorHeight,houseFacing='west'):
    if(houseFacing == 'west'):
        genHouse(x,y,z+(baseSize*2),baseSize,wallHeight, roofHeight)    #South room
        mc.setBlocks(x+int(baseSize/2),y+1,z+baseSize,x-int(baseSize/2),y+2+doorHeight,z+baseSize,0) #making door hole for south room
        genHouse(x+(baseSize*2), y, z, baseSize, wallHeight, roofHeight)    #East room
        mc.setBlocks(x+baseSize,y+1,z+int(baseSize/2),x+baseSize,y+2+doorHeight,z-int(baseSize/2),0) #making door hole for east room
        genHouse(x+(baseSize*2),y,z+(baseSize*2),baseSize,wallHeight, roofHeight)   #South-east room
        mc.setBlocks(x+(baseSize*2)+int(baseSize/2),y+1,z+baseSize,x+(baseSize*2)-int(baseSize/2),y+2+doorHeight,z+baseSize,0) #making door hole for south-east room
        mc.setBlocks(x+baseSize,y+1,z+(baseSize*2)+int(baseSize/2),x+baseSize,y+2+doorHeight,z+(baseSize*2)-int(baseSize/2),0) #making door hole for south-east room
        #North-South facing windows
        mc.setBlocks(x+int(baseSize/2),y+2,z+(baseSize*3),x-int(baseSize/2),y+wallHeight-1,z+(baseSize*3),block.STAINED_GLASS) #making window for south room
        mc.setBlocks(x+(baseSize*2)+int(baseSize/2),y+2,z+(baseSize*3),x+(baseSize*2)-int(baseSize/2),y+wallHeight-1,z+(baseSize*3),block.STAINED_GLASS) #making window for south-east room
        mc.setBlocks(x+(baseSize*2)+int(baseSize/2),y+2,z-baseSize,x+(baseSize*2)-int(baseSize/2),y+wallHeight-1,z-baseSize,block.STAINED_GLASS) #making window for east room
        #East-West facing windows
        mc.setBlocks(x+(baseSize*3),y+2,z+(baseSize*2)+int(baseSize/2),x+(baseSize*3),y+wallHeight-1,z+(baseSize*2)-int(baseSize/2),block.STAINED_GLASS) #making window for south-east room
        mc.setBlocks(x+(baseSize*3),y+2,z+int(baseSize/2),x+(baseSize*3),y+wallHeight-1,z-int(baseSize/2),block.STAINED_GLASS) #making window for east room
        mc.setBlocks(x-baseSize,y+2,z+(baseSize*2)+int(baseSize/2),x-baseSize,y+wallHeight-1,z+(baseSize*2)-int(baseSize/2),block.STAINED_GLASS) #making window for south room
    elif(houseFacing == 'east'):
        genHouse(x,y,z-(baseSize*2),baseSize,wallHeight, roofHeight)    #North room
        mc.setBlocks(x+int(baseSize/2),y+1,z-baseSize,x-int(baseSize/2),y+2+doorHeight,z-baseSize,0) #making door hole for north room
        genHouse(x-(baseSize*2),y,z,baseSize,wallHeight, roofHeight)    #West room
        mc.setBlocks(x-baseSize,y+1,z+int(baseSize/2),x-baseSize,y+2+doorHeight,z-int(baseSize/2),0) #making door hole for west room
        genHouse(x-(baseSize*2),y,z-(baseSize*2),baseSize,wallHeight, roofHeight)    #North-West room
        mc.setBlocks(x-baseSize,y+1,z+int(baseSize/2)-(baseSize*2),x-baseSize,y+2+doorHeight,z-int(baseSize/2)-(baseSize*2),0) #making door hole for n-w room
        mc.setBlocks(x+int(baseSize/2)-(baseSize*2),y+1,z-baseSize,x-int(baseSize/2)-(baseSize*2),y+2+doorHeight,z-baseSize,0) #making door hole for n-w room
        #North-South facing windows
        mc.setBlocks(x+int(baseSize/2),y+2,z-(baseSize*3),x-int(baseSize/2),y+wallHeight-1,z-(baseSize*3),block.STAINED_GLASS) #making window for north room
        mc.setBlocks(x-(baseSize*2)+int(baseSize/2),y+2,z-(baseSize*3),x-(baseSize*2)-int(baseSize/2),y+wallHeight-1,z-(baseSize*3),block.STAINED_GLASS) #making window for north-west room
        mc.setBlocks(x-(baseSize*2)+int(baseSize/2),y+2,z+baseSize,x-(baseSize*2)-int(baseSize/2),y+wallHeight-1,z+baseSize,block.STAINED_GLASS) #making window for west room
        #East-West facing windows
        mc.setBlocks(x-(baseSize*3),y+2,z+int(baseSize/2),x-(baseSize*3),y+wallHeight-1,z-int(baseSize/2),block.STAINED_GLASS)  #making window for west room
        mc.setBlocks(x-(baseSize*3),y+2,z-(baseSize*2)+int(baseSize/2),x-(baseSize*3),y+wallHeight-1,z-(baseSize*2)-int(baseSize/2),block.STAINED_GLASS)  #making window for north-west room
        mc.setBlocks(x+baseSize,y+2,z-(baseSize*2)+int(baseSize/2),x+baseSize,y+wallHeight-1,z-(baseSize*2)-int(baseSize/2),block.STAINED_GLASS)  #making window for north room

    elif(houseFacing == 'north'):
        genHouse(x-(baseSize*2),y,z,baseSize,wallHeight, roofHeight)    #West room
        mc.setBlocks(x-baseSize,y+1,z+int(baseSize/2),x-baseSize,y+2+doorHeight,z-int(baseSize/2),0) #making door hole for west room
        genHouse(x,y,z+(baseSize*2),baseSize,wallHeight, roofHeight)    #South room
        mc.setBlocks(x+int(baseSize/2),y+1,z+baseSize,x-int(baseSize/2),y+2+doorHeight,z+baseSize,0) #making door hole for south room
        genHouse(x-(baseSize*2),y,z+(baseSize*2),baseSize,wallHeight, roofHeight)   #South-West Room
        mc.setBlocks(x-baseSize,y+1,z+int(baseSize/2)+(baseSize*2),x-baseSize,y+2+doorHeight,z-int(baseSize/2)+(baseSize*2),0) #making door hole for south-west room
        mc.setBlocks(x+int(baseSize/2)-(baseSize*2),y+1,z+baseSize,x-int(baseSize/2)-(baseSize*2),y+2+doorHeight,z+baseSize,0) #making door hole for south-west room
        #North-South facing windows
        mc.setBlocks(x-(baseSize*2)+int(baseSize/2),y+2,z-(baseSize),x-(baseSize*2)-int(baseSize/2),y+wallHeight-1,z-(baseSize),block.STAINED_GLASS) #making window for west room
        mc.setBlocks(x-(baseSize*2)+int(baseSize/2),y+2,z+(baseSize*3),x-(baseSize*2)-int(baseSize/2),y+wallHeight-1,z+(baseSize*3),block.STAINED_GLASS) #making window for south-west room
        mc.setBlocks(x+int(baseSize/2),y+2,z+(baseSize*3),x-int(baseSize/2),y+wallHeight-1,z+(baseSize*3),block.STAINED_GLASS) #making window for south room
        #East-West facing windows
        mc.setBlocks(x-(baseSize*3),y+2,z+int(baseSize/2),x-(baseSize*3),y+wallHeight-1,z-int(baseSize/2),block.STAINED_GLASS)  #making window for west room
        mc.setBlocks(x-(baseSize*3),y+2,z+(baseSize*2)+int(baseSize/2),x-(baseSize*3),y+wallHeight-1,z+(baseSize*2)-int(baseSize/2),block.STAINED_GLASS)  #making window for south-west room
        mc.setBlocks(x+baseSize,y+2,z+(baseSize*2)+int(baseSize/2),x+baseSize,y+wallHeight-1,z+(baseSize*2)-int(baseSize/2),block.STAINED_GLASS)  #making window for south room
    elif(houseFacing == 'south'):
        genHouse(x+(baseSize*2), y, z, baseSize, wallHeight, roofHeight)    #East room
        mc.setBlocks(x+baseSize,y+1,z+int(baseSize/2),x+baseSize,y+2+doorHeight,z-int(baseSize/2),0) #making door hole for east room
        genHouse(x,y,z-(baseSize*2),baseSize,wallHeight, roofHeight)    #North room
        mc.setBlocks(x+int(baseSize/2),y+1,z-baseSize,x-int(baseSize/2),y+2+doorHeight,z-baseSize,0) #making door hole for north room
        genHouse(x+(baseSize*2),y,z-(baseSize*2),baseSize,wallHeight, roofHeight)    #North-east room
        mc.setBlocks(x+baseSize,y+1,z+int(baseSize/2)-(baseSize*2),x+baseSize,y+2+doorHeight,z-int(baseSize/2)-(baseSize*2),0) #making door hole for east room
        mc.setBlocks(x+int(baseSize/2)+(baseSize*2),y+1,z-baseSize,x-int(baseSize/2)+(baseSize*2),y+2+doorHeight,z-baseSize,0) #making door hole for north room
        #North-South facing windows
        mc.setBlocks(x+(baseSize*2)+int(baseSize/2),y+2,z+baseSize,x+(baseSize*2)-int(baseSize/2),y+wallHeight-1,z+baseSize,block.STAINED_GLASS) #making window for east room
        mc.setBlocks(x+(baseSize*2)+int(baseSize/2),y+2,z-(baseSize*3),x+(baseSize*2)-int(baseSize/2),y+wallHeight-1,z-(baseSize*3),block.STAINED_GLASS) #making window for north-east room
        mc.setBlocks(x+int(baseSize/2),y+2,z-(baseSize*3),x-int(baseSize/2),y+wallHeight-1,z-(baseSize*3),block.STAINED_GLASS) #making window for north room
        #East-West facing windows
        mc.setBlocks(x-baseSize,y+2,z-(baseSize*2)+int(baseSize/2),x-baseSize,y+wallHeight-1,z-(baseSize*2)-int(baseSize/2),block.STAINED_GLASS)  #making window for north room
        mc.setBlocks(x+(baseSize*3),y+2,z-(baseSize*2)+int(baseSize/2),x+(baseSize*3),y+wallHeight-1,z-(baseSize*2)-int(baseSize/2),block.STAINED_GLASS)  #making window for north-east room
        mc.setBlocks(x+(baseSize*3),y+2,z+int(baseSize/2),x+(baseSize*3),y+wallHeight-1,z-int(baseSize/2),block.STAINED_GLASS)  #making window for east room

def genStairs(x,y,z,height,width = 2,facing = 'east',mat = 1):
    offset = 1  #How close/far away the stairs end from the edge of the room
    if facing == 'south':
        z = (z+baseSize)-(height-offset)
        for i in range(0,height):
            mc.setBlocks(x-width,y+i,z+i,x+width,y+i,z,0)    #Makes air hole
            mc.setBlocks(x-width,y+i,z+i,x+width,y+i,z+i,mat,2)
    elif facing == 'east':
        x = (x+baseSize)-(height-offset)
        for i in range(0,height):
            mc.setBlocks(x+i,y+i,z-width,x,y+i,z+width,0)    #Makes air hole
            mc.setBlocks(x+i,y+i,z-width,x+i,y+i,z+width,mat,0)
    elif facing == 'west':
        x = (x-baseSize)+(height-offset)
        for i in range(0,height):
            mc.setBlocks(x-i,y+i,z-width,x,y+i,z+width,0)    #Makes air hole
            mc.setBlocks(x-i,y+i,z-width,x-i,y+i,z+width,mat,1)
    elif facing == 'north':
        z = (z-baseSize)+(height-offset)
        for i in range(0,height):
            mc.setBlocks(x-width,y+i,z-i,x+width,y+i,z,0)     #Makes air hole
            mc.setBlocks(x-width,y+i,z-i,x+width,y+i,z-i,mat,3)
    else:
        print('invalid direction')


def genFirePit(x,y,z,mat):
    mc.setBlocks(x-1,y,z-1,x-1,y,z+1,mat,0)
    mc.setBlocks(x+1,y,z-1,x+1,y,z+1,mat,1)
    mc.setBlock(x,y,z-1,mat,2)
    mc.setBlock(x,y,z+1,mat,3)
    mc.setBlock(x,y-1,z,block.NETHERRACK)
    mc.setBlock(x,y,z,block.FIRE)

def get_compass_direction():
    angle = mc.player.getRotation()
    if 90 + 45 < angle <= 180 + 45:
        return "north"
    if 180 + 45 < angle <= 270 + 45:
        return "east"
    if 270 + 45 < angle <= 360 or angle <= 45:
        return "south"
    if 0 + 45 < angle <= 90 + 45:
        return "west"

genHouse(x,y,z-20,baseSize,wallHeight, roofHeight,True, dir=get_compass_direction())