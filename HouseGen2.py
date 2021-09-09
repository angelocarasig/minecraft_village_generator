from vec3 import Vec
from mcpi import minecraft
from mcpi.minecraft import Minecraft
from mcpi import block

mc = Minecraft.create()

pos = mc.player.getPos()

# North: -ve Z
# South: +ve Z
# West: -ve X
# East: +ve X

# Get Opposite Direction
def GetOppositeDirection(direction):
    if direction == "N":
        return "S"
    elif direction == "S":
        return "N"
    elif direction == "W":
        return "E"
    elif direction == "E":
        return "W"

def GetVectorFromDirection(direction):
    if direction == "N":
        return Vec(0, 0, -1)
    elif direction == "S":
        return Vec(0, 0, 1)
    elif direction == "W":
        return Vec(-1, 0, 0)
    elif direction == "E":
        return Vec(1, 0, 0)

# House > Level > Room
class House():
    def __init__(self, x, y, z, direction="N", roomSize=5, roomHeight=3):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.direction = direction
        self.roomSize = roomSize
        self.roomHeight = roomHeight
        self.levels = []
        self.rooms = []
    
    def CreateLevel(self):
        yHeight = self.y
        newLevel = Level(self, yHeight)
        self.levels.append(newLevel)
        return newLevel

# Contains rooms
class Level():
    def __init__(self, house, yHeight):
        self.house = house
        self.rooms = []
        self.yHeight = yHeight

    def CreateRoom(self, origin=None):
        newRoom = Room(self, origin)
        self.rooms.append(newRoom)
        return newRoom
    
    def GenerateDoorways(self):
        complete = []

        for room in self.rooms:
            halfSize = self.house.roomSize // 2
            roomCenter = room.origin + Vec(halfSize, 0, halfSize)

            mc.setBlock(roomCenter.x, roomCenter.y, roomCenter.z, block.GLOWSTONE_BLOCK.id)
            
            for adjRoomData in room.adjacentRooms:
                adjRoom = adjRoomData[0]
                adjDirection = adjRoomData[1]

                # Doorway already created
                if adjRoom in complete:
                    continue

                doorPos = roomCenter + GetVectorFromDirection(adjDirection) * (self.house.roomSize // 2 + 1)
                doorHeightY = doorPos.y + self.house.roomHeight - 1
                halfDoorWidth = self.house.roomSize / 2 - 1

                # Clear doorway
                if adjDirection == "N" or adjDirection == "S":
                    mc.setBlocks(
                        doorPos.x - halfDoorWidth + 1, doorPos.y, doorPos.z,
                        doorPos.x + halfDoorWidth, doorHeightY, doorPos.z,
                        block.AIR.id
                    )

                    # Add floor
                    mc.setBlocks(
                        doorPos.x - halfDoorWidth + 1, doorPos.y, doorPos.z,
                        doorPos.x + halfDoorWidth, doorPos.y, doorPos.z,
                        1
                    )
                elif adjDirection == "W" or adjDirection == "E":
                    mc.setBlocks(
                        doorPos.x, doorPos.y, doorPos.z - halfDoorWidth + 1,
                        doorPos.x, doorHeightY, doorPos.z + halfDoorWidth,
                        block.AIR.id
                    )

                    # Add floor
                    mc.setBlocks(
                        doorPos.x, doorPos.y, doorPos.z - halfDoorWidth + 1,
                        doorPos.x, doorPos.y, doorPos.z + halfDoorWidth,
                        1
                    )

                mc.setBlock(doorPos.x, doorPos.y, doorPos.z, block.GLOWSTONE_BLOCK.id)

            complete.append(room)


class Room():
    def __init__(self, level, origin=None):
        self.level = level
        self.house = self.level.house
        self.adjacentRooms = []

        self.origin = origin if origin != None else Vec(self.house.x, self.level.yHeight, self.house.z)
        self.CreateFloor()
        self.CreateWalls()
    
    def CreateFloor(self):
        mc.setBlocks(
            self.origin.x, self.origin.y, self.origin.z,
            self.origin.x + self.house.roomSize - 1, self.origin.y, self.origin.z + self.house.roomSize - 1,
            1
        )
    
    def CreateWalls(self):
        cornerOrigin = self.origin - Vec(1, 0, 1)
        cornerOrigin2 = self.origin + Vec(self.house.roomSize, 0, self.house.roomSize)
        wallHeightY = self.origin.y + self.house.roomHeight

        # NW Corner
        mc.setBlocks(
            cornerOrigin.x, cornerOrigin.y, cornerOrigin.z,
            cornerOrigin.x + self.house.roomSize + 1, wallHeightY, cornerOrigin.z,
            block.WOOD_PLANKS.id
        )
        mc.setBlocks(
            cornerOrigin.x, cornerOrigin.y, cornerOrigin.z,
            cornerOrigin.x, wallHeightY, cornerOrigin.z + self.house.roomSize + 1,
            block.WOOD_PLANKS.id
        )

        # SE Corner
        mc.setBlocks(   
            cornerOrigin2.x, cornerOrigin2.y, cornerOrigin2.z,
            cornerOrigin2.x - self.house.roomSize, wallHeightY, cornerOrigin2.z,
            block.WOOD_PLANKS.id
        )
        mc.setBlocks(   
            cornerOrigin2.x, cornerOrigin2.y, cornerOrigin2.z,
            cornerOrigin2.x, wallHeightY, cornerOrigin2.z - self.house.roomSize,
            block.WOOD_PLANKS.id
        )
        

    def AddAdjacentRoom(self, direction):
        for adj in self.adjacentRooms:
            adjDirection = adj[1]
            if direction == adjDirection:
                print("Room clashes with existing room. New room not created")
                return -1

        origin = self.origin
        sizeAmount = self.house.roomSize + 1
        if direction == "N":
            origin = origin - Vec(0, 0, sizeAmount)
        elif direction == "S":
            origin = origin + Vec(0, 0, sizeAmount)
        elif direction == "W":
            origin = origin - Vec(sizeAmount, 0, 0)
        elif direction == "E":
            origin = origin + Vec(sizeAmount, 0, 0)

        newRoom = self.level.CreateRoom(origin)
        newRoom.adjacentRooms.append([self, GetOppositeDirection(direction)])
        self.adjacentRooms.append([newRoom, direction])

        return self.level.CreateRoom(origin)

# Build house
myHouse = House(pos.x, pos.y - 5, pos.z, "N", 9, 4)
groundLevel = myHouse.CreateLevel()
room1 = groundLevel.CreateRoom()
room2 = room1.AddAdjacentRoom("E")
room3 = room1.AddAdjacentRoom("S")
room4 = room1.AddAdjacentRoom("W")

groundLevel.GenerateDoorways()

#secondFloor = myHouse.CreateFloor()
#room2 = secondFloor.CreateRoom()