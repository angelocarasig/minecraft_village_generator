from mcpi.minecraft import Minecraft
from mcpi import block as Block
from vec3 import Vec
from threading import Thread

mc = Minecraft.create()

air = Block.AIR.id

threads = []

# Size of area to clear
area_size = Vec(30, 0, 30)

# Player pos
x, y, z = mc.player.getPos()

# Adjust origin so bounding box centers on player
cx = int(x - area_size.x / 2)
cy = int(y - area_size.y / 2)
cz = int(z - area_size.z / 2)

def CheckHighestBlock(x, z):
    new_mc = Minecraft.create()

    height = new_mc.getHeight(x, z)
    DeleteTreeBlocksRecursive(x, height, z)

def DeleteTreeBlocksRecursive(x, y, z):
    new_mc = Minecraft.create()

    curr_block = new_mc.getBlock(x, y, z)

    # Logs or leaves
    tree_cond = curr_block == 17 or curr_block == 18
    air_cond = curr_block == air

    # Base case
    if not tree_cond:
        return
    elif air_cond:
        # Air
        DeleteTreeBlocksRecursive(x, y - 1, z)
    else:
        # Logs or Leaves
        mc.setBlock(x, y, z, air)
        DeleteTreeBlocksRecursive(x, y - 1, z)


print("Clearing Trees...")

# super slow for large areas
# TODO: Multithreading?
def ClearTrees(min_x, max_x, min_z, max_z):
    for ix in range(min_x, max_x):
        for iz in range(min_z, max_z):
            thread = Thread(target=CheckHighestBlock, args=(ix, iz))

            thread.start()

            if iz == max_z:
                thread.join()

ClearTrees(cx, cx + area_size.x, cz, cz + area_size.z)

'''
subdivisions = 4

for x in range(subdivisions):
    for z in range(subdivisions):
        ClearTrees(
            cx + area_size.x // subdivisions * (x - 1),
            cx + area_size.x // subdivisions * x,
            cz + area_size.z // subdivisions * (z - 1),
            cz + area_size.z // subdivisions * z
        )
'''

print("Trees cleared")