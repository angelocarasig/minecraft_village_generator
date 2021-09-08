from mcpi.minecraft import Minecraft
from mcpi import block
import concurrent.futures
import threading
import random
import math

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

#TODO: Change setBlock to setBlocks to make it maybe faster
#TODO: Make paths longer and vary in amount of side paths

LENGTH = 20

x, y, z = mc.player.getPos()

def path_builder(x, y, z, direction="North"):
    seed_random = 1
    for _ in range(20):
        curr_block = mc.getBlock(x, y - 1, z)
        
        #Check if above blocks exist
        inc_count = 0
        above_block = mc.getBlock(x, y, z)
        while above_block != 0:
            inc_count += 1
            mc.postToChat("Block above exists, increasing y by 1")
            if inc_count > 8:
                mc.postToChat("Position too low")
                break
            y += 1
            above_block = mc.getBlock(x, y, z)

        #Check for cliffs
        dec_count = 0
        while curr_block == 0:
            dec_count += 1
            if dec_count > 8:
                mc.postToChat("Buffer: " + str(dec_count))
                mc.postToChat("Cliff face too steep to continue")
                break
            mc.postToChat("Met air, decreasing y by 1")
            y -= 1
            curr_block = mc.getBlock(x, y - 1, z)
            mc.postToChat(curr_block)
        
        #If cliffs or caves hit a limit
        if dec_count > 8 or inc_count > 8:
            mc.postToChat("Exiting village generation...")
            break

        mc.setBlock(x, y - 1, z, 208)
        

        seed = random.randint(1,100)
        if 0.1*(math.e**seed_random) > seed:
            temp_val = random.randint(0,1)
            if direction == "North" or direction == "South":
                if temp_val == 0:
                    mc.setBlocks(x-1, y-1, z, x-4, y-1, z, block.COBBLESTONE)
                else:
                    mc.setBlocks(x+1, y-1, z, x+4, y-1, z, block.COBBLESTONE)
            else:
                if temp_val == 0:
                    mc.setBlocks(x, y-1, z-1, x, y-1, z-4, block.COBBLESTONE)
                else:
                    mc.setBlocks(x, y-1, z+1, x, y-1, z+4, block.COBBLESTONE)
            seed_random = 0
        else:
            seed_random += 1

        #Continue in direction
        if direction == "North":
            z -= 1
        elif direction == "East":
            x += 1
        elif direction == "South":
            z += 1
        else:
            x -= 1

# directions = ["North", "East", "South", "West"]

# # for direction in directions:
# #     thread = threading.Thread(target=path_builder, args=(direction,))
# #     thread.start()

# #     #For some reason we can't let the threads go at the same time, no clue why
# #     thread.join()

# for direction in directions:
#     path_builder(x, y, z, direction)