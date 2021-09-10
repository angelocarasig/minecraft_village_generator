from mcpi import minecraft
from mcpi.minecraft import Minecraft
from mcpi import block
import concurrent.futures
import threading
import random
import math

def get_compass_direction():
    mc = Minecraft.create()
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

LENGTH = 20


# x, y, z = mc.player.getPos()

def path_builder(x, y, z, direction="North"):
    mc = Minecraft.create()
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


#Solo testing:
directions = ["North", "East", "South", "West"]

curr_pos_x, curr_pos_y, curr_pos_z = minecraft.Minecraft.create().player.getPos()

for direction in directions:
    thread = threading.Thread(target=path_builder, args=(curr_pos_x, curr_pos_y, curr_pos_z, direction,))
    thread.start()


thread_1 = threading.Thread(target=path_builder, args=(curr_pos_x, curr_pos_y, curr_pos_z, "North",))
thread_2 = threading.Thread(target=path_builder, args=(curr_pos_x, curr_pos_y, curr_pos_z, "East",))
thread_3 = threading.Thread(target=path_builder, args=(curr_pos_x, curr_pos_y, curr_pos_z, "South",))
thread_4 = threading.Thread(target=path_builder, args=(curr_pos_x, curr_pos_y, curr_pos_z, "West",))

thread_1.start()
thread_2.start()
thread_3.start()
thread_4.start()


#     #For some reason we can't let the threads go at the same time, no clue why
#     thread.join()