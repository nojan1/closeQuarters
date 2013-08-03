import random, math
from pygame import Rect
from geometry import getAngleDistance

##### CONFIG #####

WORLDSIZE = (70, 50)

ROOMMAX = 15
ROOMMIN = 9

NUMROOMSMIN = 3
NUMROOMSMAX = 5

ROOMSPACING = 10
MAXROOMALLOCATTEMPTS = 1000

CORTHICKNESS = 4

##################

def makeCor(start, end, grid, joinUp = False):
    angle, distance = getAngleDistance(start, end)
    angle = int(math.degrees(angle))
    if angle < 0:
        angle += 360

    angleIndex = int((angle % 360) / 90) 
    increments = [(1,0), (0,1), (-1,0), (0,-1)]

    increment = increments[int(angleIndex)]

    if joinUp:
        start = ( start[0] + int((increment[0] * -1) * (CORTHICKNESS / 2)), start[1] + int((increment[1] * -1) * (CORTHICKNESS / 2)) )
        distance = getAngleDistance(start, end)[1]

    iMin = int((CORTHICKNESS / 2) * -1) - 1
    iMax = int(CORTHICKNESS / 2)
    for i in range(iMin, iMax + 1):
        sX = start[0] + (i * increment[1])
        sY = start[1] + (i * increment[0])

        for z in range(int(distance)):
            x = sX + (z * increment[0])
            y = sY + (z * increment[1])
            try:
                if (i == iMin or i == iMax) and grid[x][y] != "#":
                    grid[x][y] = "W"
                elif grid[x][y] != "?": 
                    grid[x][y] = "#"
            except:
                print("Out of bounds %i,%i" % (x,y))
        
            

numRooms = random.randint(NUMROOMSMIN, NUMROOMSMAX)
roomInfo = []

#Fill grid with EMPTY
mapGrid = []
for x in range(WORLDSIZE[0] + 2):
    row = []
    for y in range(WORLDSIZE[1] + 2):
        row.append(".")
    
    mapGrid.append(row)

#Generate rooms
for roomID in range(numRooms):
    attempts = 0
    room = Rect(0,0,0,0)
    room.width = random.randint(ROOMMIN, ROOMMAX)
    room.height = random.randint(ROOMMIN, ROOMMAX)

    posFound = False
    while not posFound:
        if attempts == MAXROOMALLOCATTEMPTS:
            print("Could not resolve room placement for room %i, bailing" % (roomID+1))
            break

        room.x = random.randint(1, WORLDSIZE[0] - 1)
        room.y = random.randint(1, WORLDSIZE[1] - 1)

        if (room.x + room.width) >= (WORLDSIZE[0] - 1) or (room.y + room.height) >= (WORLDSIZE[1] - 1):
            attempts += 1
            continue

        posFound = True

        for r,w in roomInfo:
            if r.inflate(2*ROOMSPACING, 2*ROOMSPACING).colliderect(room):
                posFound = False
                attempts += 1
                break

    if not posFound:
        continue 

    #Place waypoint
    wpX = random.randint(room.x + 1 + int(CORTHICKNESS / 2), room.x + room.width - 1 - int(CORTHICKNESS / 2))
    wpY = random.randint(room.y + 1 + int(CORTHICKNESS / 2), room.y + room.height - 1 - int(CORTHICKNESS / 2) )
    roomInfo.append( (room, (wpX, wpY)) )

    for x in range(room.x, room.x + room.width):
        for y in range(room.y, room.y + room.height):
            if x == room.x or x == (room.x + room.width - 1) or y == room.y or y == (room.y + room.height - 1):
                mapGrid[x][y] = "W"
            else:
                if random.randint(0,100) < 10:
                    mobChar = list(["Z", "S"])[random.randint(0,1)]
                    mapGrid[x][y] = mobChar
                else:
                    mapGrid[x][y] = "#"

    mapGrid[wpX][wpY] = "?"

print("Placed %i rooms" % len(roomInfo))

#Generate corridors
for r, w in roomInfo:
    distance = -1
    nearest = []
    for r2, w2 in roomInfo:
        if r2 == r:
            continue

        angle, newDistance = getAngleDistance(w, w2)
        if distance == -1 or newDistance < distance:
            distance = newDistance
            nearest = (r2, w2)

    #Only needs one coridor?
    roomInfo.remove( (r2, w2) )

    print("Needs to make coridor between %s and %s" % (w, nearest[1]))
    if math.degrees(angle) % 90 == 0:
        print(" - Direct line detected, using simple algoritm")
        makeCor(w, nearest[1], mapGrid)
    else:
        print(" - Needs to bend the line")
        if abs(w[0] - nearest[1][0]) < abs(w[1] - nearest[1][1]):
            #Bend for X
            makeCor(w,(w[0], nearest[1][1]), mapGrid)
            makeCor((w[0], nearest[1][1]), nearest[1], mapGrid, True)
        else:
            #Bend for Y
            makeCor(w, (nearest[1][0], w[1]), mapGrid)
            makeCor((nearest[1][0], w[1]), nearest[1], mapGrid, True)



#Output map file
f = open("map.lvl", "w")
for y in range(WORLDSIZE[1] + 2):
    row = ""
    for x in range(WORLDSIZE[0] + 2):
        row += mapGrid[x][y]

    f.write(row + "\n")

f.close()
