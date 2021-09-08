from mcpi.minecraft import Minecraft
from mcpi import block as Block
from vec3 import Vec

mc = Minecraft.create()

air = Block.AIR.id

# Size of area to clear
area_size = Vec(10, 10, 10)

# Player pos
x, y, z = mc.player.getPos()

# Adjust origin so bounding box centers on player
cx = int(x - area_size.x / 2)
cy = int(y - area_size.y / 2)
cz = int(z - area_size.z / 2)

def CheckHighestBlock(x, z):
    height = mc.getHeight(x, z)
    DeleteTreeBlocksRecursive(x, height, z)

def DeleteTreeBlocksRecursive(x, y, z):
    curr_block = mc.getBlock(x, y, z)

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
def ClearTrees():
    for ix in range(cx, cx + area_size.x):
        for iz in range(cz, cz + area_size.z):
            CheckHighestBlock(ix, iz) # waits until this is complete before moving to next block

ClearTrees()

print("Trees cleared")