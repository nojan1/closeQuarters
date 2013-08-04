import random, math, sys
from pygame import Rect
from geometry import getAngleDistance
from config import *

class LevelGenerator(object):
    def __init__(self):
        self.roomInfo = []
        self.playerPos = (0,0)

        #Fill grid with EMPTY
        self.mapGrid = []
        for x in range(WORLDSIZE[0] + 2):
            row = []
            for y in range(WORLDSIZE[1] + 2):
                row.append(".")
    
            self.mapGrid.append(row)

        self.makeRooms()
        self.makeCor()
        self.makeEntries()
        self.makeSpecials()
        self.makeWalls()

    def makeRooms(self):
        numRooms = random.randint(NUMROOMSMIN, NUMROOMSMAX)
         
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

                room.x = random.randint(2, WORLDSIZE[0] - 1)
                room.y = random.randint(5, WORLDSIZE[1] - 1)

                if (room.x + room.width) >= (WORLDSIZE[0] - 1) or (room.y + room.height) >= (WORLDSIZE[1] - 4):
                    attempts += 1
                    continue

                posFound = True

                for r,w in self.roomInfo:
                    if r.inflate(2*ROOMSPACING, 2*ROOMSPACING).colliderect(room):
                        posFound = False
                        attempts += 1
                        break

            if not posFound:
                continue 

            #Place waypoint
            wpX = random.randint(room.x + 1 + int(CORTHICKNESS / 2), room.x + room.width - 1 - int(CORTHICKNESS / 2))
            wpY = random.randint(room.y + 1 + int(CORTHICKNESS / 2), room.y + room.height - 1 - int(CORTHICKNESS / 2) )
            self.roomInfo.append( (room, (wpX, wpY)) )

            for x in range(room.x, room.x + room.width):
                for y in range(room.y, room.y + room.height):
                    self.mapGrid[x][y] = "#"

        #Sort rooms in order of Y coordinates
        self.roomInfo.sort(key=lambda r: r[0].y)
        print("Placed %i rooms" % len(self.roomInfo))

    def makeCor(self):
        #Generate corridors
        for r, w in self.roomInfo:
            distance = -1
            nearest = []
            for r2, w2 in self.roomInfo:
                if r2 == r:
                    continue

                angle, newDistance = getAngleDistance(w, w2)
                if distance == -1 or newDistance < distance:
                    distance = newDistance
                    nearest = (r2, w2)

            #Only needs one coridor?
            #roomInfo.remove( (r2, w2) )

            print("Needs to make coridor between %s and %s" % (w, nearest[1]))
            if math.degrees(angle) % 90 == 0:
                print(" - Direct line detected, using simple algoritm")
                self.placeCor(w, nearest[1])
            else:
                print(" - Needs to bend the line")
                if abs(w[0] - nearest[1][0]) < abs(w[1] - nearest[1][1]):
                    #Bend for X
                    self.placeCor(w,(w[0], nearest[1][1]))
                    self.placeCor((w[0], nearest[1][1]), nearest[1], True)
                else:
                    #Bend for Y
                    self.placeCor(w, (nearest[1][0], w[1]))
                    self.placeCor((nearest[1][0], w[1]), nearest[1], True)

    def placeCor(self, start, end, joinUp = False):
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

        iMin = int((CORTHICKNESS / 2) * -1)
        iMax = int(CORTHICKNESS / 2)
        for i in range(iMin, iMax + 1):
            sX = start[0] + (i * increment[1])
            sY = start[1] + (i * increment[0])

            for z in range(int(distance)):
                x = sX + (z * increment[0])
                y = sY + (z * increment[1])
                try:
                    if self.mapGrid[x][y] != "?": 
                        self.mapGrid[x][y] = "#"
                except:
                    print("Out of bounds %i,%i" % (x,y))
        
    def makeEntries(self):
        #Add specials
        length = CORTHICKNESS
        x1 = self.roomInfo[0][0].x + int(self.roomInfo[0][0].width / 2)
        y1 = self.roomInfo[0][0].y

        x2 = self.roomInfo[-1][0].x + int(self.roomInfo[-1][0].width / 2)
        y2 = self.roomInfo[-1][0].y + self.roomInfo[-1][0].height - 1

        for i in range(length):
            self.mapGrid[x1 + i][y1 - 1] = "#"
            self.mapGrid[x1 + i][y1 - 2] = "#"
            self.mapGrid[x1 + i][y1 - 3] = "-"

            self.mapGrid[x2 + i][y2 + 1] = "#"
            self.mapGrid[x2 + i][y2 + 2] = "#"
            self.mapGrid[x2 + i][y2 + 3] = "+"

        self.mapGrid[x1 + int(length / 2)][y1-2] = "P"
        self.playerPos = (x1 + int(length / 2), y1 - 2)
            

    def makeSpecials(self):
        #Add mobs and pickups
        for i in range(random.randint(MOBMIN, MOBMAX)):
            pos = (-1,-1)
            while pos == (-1,-1) or self.mapGrid[pos[0]][pos[1]] != "#" or getAngleDistance(self.playerPos, pos)[1] < MOBTOPLAYERTHRESHOLD:
                pos = ( random.randint(2, WORLDSIZE[0] - 1), random.randint(2, WORLDSIZE[1] - 1) )

            if random.randint(0,100) > 90:
                #place pickup
                char = list(["L", "R", "H"])[random.randint(0,2)]
            else:
                char = list(["Z", "Z", "S"])[random.randint(0,2)]
    
            self.mapGrid[pos[0]][pos[1]] = char        

    def makeWalls(self):
        #Add the walls
        nonFloors = ("#", "Z", "S", "P", "H", "R", "L")
        for y in range(1,WORLDSIZE[1] + 1):
            for x in range(1,WORLDSIZE[0] + 1):
                if self.mapGrid[x][y] == "." and (self.mapGrid[x][y+1] in nonFloors or self.mapGrid[x+1][y] in nonFloors or self.mapGrid[x][y-1] in nonFloors or self.mapGrid[x-1][y] in nonFloors or self.mapGrid[x+1][y+1] in nonFloors or self.mapGrid[x+1][y-1] in nonFloors or self.mapGrid[x-1][y-1] in nonFloors or self.mapGrid[x-1][y+1] in nonFloors):
                    self.mapGrid[x][y] = "W"


    def generateOutput(self):
        data = ""
        for y in range(WORLDSIZE[1] + 2):
            row = ""
            for x in range(WORLDSIZE[0] + 2):
                row += self.mapGrid[x][y]

            if y == 0 or y == (WORLDSIZE[1] + 1) or row.strip().replace(".", "") != "":
                data += row + "\n"

        return data


if __name__ == "__main__":
    level = LevelGenerator()
    data = level.generateOutput()

    if len(sys.argv) < 2 or sys.argv[1] == "-":
        print(data)
    else:
        #Output map file
        f = open(sys.argv[1], "w")
        f.write(data)
        f.close()
