from mcpi import minecraft

mc = minecraft.Minecraft.create()

x, y, z = mc.player.getPos()
#Constants
half = 50 #Half the width of the cube generated
treeStuff = [0, 18, 161, 17, 162, 99, 100] #Item ID's that should not be counted as floor (for stair generation)
amountOut = 10 #How long the staris should extend out to the circle

def clearLand(x,y,z):   #Clear land
    currHeight = mc.getHeight(x, z)
    lowest = currHeight
    avSum = 0
    timesRun = 0
    for i in range(-half,half,10):
        if mc.getHeight(x+i,z+half) < lowest:
            lowest = mc.getHeight(x+i,z+half)
        avSum += mc.getHeight(x+i,z+half)
        if mc.getHeight(x+i,z-half) < lowest:
            lowest = mc.getHeight(x+i,z-half)
        avSum += mc.getHeight(x+i,z-half)
        if mc.getHeight(x+half,z+i) < lowest:
            lowest = mc.getHeight(x+half,z+i)
        avSum += mc.getHeight(x+half,z+i)
        if mc.getHeight(x-half,z+i) < lowest:
            lowest = mc.getHeight(x-half,z+i)
        avSum += mc.getHeight(x-half,z+i)
        timesRun += 1
    ave = int(avSum/timesRun)
    print('ave: ' + str(ave))
    print('Lowest: ' + str(lowest))
    if abs(lowest - ave) > 30:
        print(abs(lowest - ave))
        print('too low')
        lowest = y - 10

    mc.setBlocks(x-half,lowest,z-half,x+half,currHeight+100,z+half,0)
    mc.setBlocks(x-half,lowest,z-half,x+half,lowest,z+half,2)
    return lowest

def generateStairs(x,y,z,lowest,axis,dir=1):
    if axis == 'x':
        newx = x
        newz = z
        for j in range(0,100,2):
            currHeight = lowest
            top = mc.getHeight(newx,newz+j)
            if top < lowest:
                mc.setBlocks(newx,-90,newz+j,newx,currHeight-1,newz+j+1,1)
                continue
            while mc.getBlock(newx,top,newz+j) in treeStuff:
                top = top - 1
            if top < lowest:
                top = lowest
            step = int((top-lowest)/amountOut)
            remainder = (top-lowest)%amountOut
            for i in range(amountOut,0,-1):
                if (i - remainder) > 0:
                    mc.setBlocks(newx+(i*dir),lowest,newz+j,newx+(i*dir),currHeight+step,newz+j+2,2)
                    currHeight = currHeight+step
                else:
                    mc.setBlocks(newx+(i*dir),lowest,newz+j,newx+(i*dir),currHeight+step+1,newz+j+2,2)
                    currHeight = currHeight+step+1
    elif axis == 'y':
        newx = x
        newz = z
        for j in range(0,100,2):
            currHeight = lowest
            top = mc.getHeight(newx+j,newz)
            if top < lowest:
                mc.setBlocks(newx+j,-91,newz,newx+j+1,currHeight - 1,newz,1)
                continue
            while mc.getBlock(newx+j,top,newz) in treeStuff:
                top = top - 1
            if top < lowest:
                top = lowest
            step = int((top-lowest)/amountOut)
            remainder = (top-lowest)%amountOut
            for i in range(amountOut,0,-1):
                if (i - remainder) > 0:
                    mc.setBlocks(newx+j,lowest,newz+(i*dir),newx+j+2,currHeight+step,newz+(i*dir),2)
                    currHeight = currHeight+step
                else:
                    mc.setBlocks(newx+j,lowest,newz+(i*dir),newx+j+2,currHeight+step+1,newz+(i*dir),2)
                    currHeight = currHeight+step+1

def buildFoundation(x,y,z):
    lowest = clearLand(x,y,z)
    generateStairs(x-(half+1),y,z-half,lowest,'x',1)
    generateStairs(x+(half+1),y,z-half,lowest,'x',-1)
    generateStairs(x-half,y,z-(half+1),lowest,'y',1)
    generateStairs(x-half,y,z+(half+1),lowest,'y',-1)

