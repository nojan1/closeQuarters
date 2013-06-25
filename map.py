import os

from tile import *
from config import *
from zombie import *

class Map(object):
    def __init__(self):
        self.tiles = None
        self.mobs = []

    def loadLevel(self, levelID):
        self.tiles = []
        
        path = os.path.join(LEVELPATH, str(levelID)+".lvl")
        if not os.path.exists(path):
            raise Exception("No such levelfile;", path)

        for yPos,line in enumerate(open(path, "r")):
            x = []
            for xPos, char in enumerate(line.strip()):
                pos = (xPos, yPos)
                if char == ".":
                    x.append(Empty(pos))
                elif char == "#":
                    x.append(Floor(pos))
                elif char == "W":
                    x.append(Wall(pos))
                elif char == "Z":
                    #Group of mobs, how many depends on dificulty
                    self.allocateMobs(pos, 10, Zombie)
                    
                    #Fill in blank with floor
                    x.append(Floor(pos))
                else:
                    print("Warning: Unknown tile; ", char)

            self.tiles.append(x)
            
    def drawMobsInView(self, screen, game):
        for m in self.mobs:
            if m.getRect().colliderect(game.getView()):
                m.draw(screen, game)

    def drawTilesInView(self, screen, game):
        for y in self.tiles:
            for tile in y:
                if tile != None and tile.getRect().colliderect(game.getView()):
                    tile.draw(screen, game)

    def isAllowedPosition(self, rectToCheck):
        for y in self.tiles:
            for tile in y:
                if tile != None and tile.getRect().colliderect(rectToCheck):
                    if tile.onCollision():
                        return False

        return True

    def mobWasHit(self, mobHitted, weapon):
        if mobHitted.takeDamage(weapon.damage):
            self.mobs.remove(mobHitted)

    def mobPresent(self, pos):
        for m in self.mobs:
            if m.pos == pos:
                return True
        
        return False

    def allocateMobs(self, tileCoords, numMobs, mobClass):
        basePos = (tileCoords[0] * TILESIZE[0], tileCoords[1] * TILESIZE[1])

        posDirs = [(0,-1), (1,0), (0,1), (-1,0)]

        for i in range(numMobs):
            testMob = mobClass(basePos)
            if self.mobPresent(basePos):
                #Find new pos
                addedDistance = 0
                while 1:
                    addedDistance += testMob.getRect().width
                    newPos = (basePos[0] + (posDirs[0][0] * addedDistance), basePos[1] + (posDirs[0][1] * addedDistance))
                    testMob = mobClass(newPos)
                
                    if not self.isAllowedPosition(testMob.getRect()):
                        posDirs.pop(0)
                        if len(posDirs) == 0:
                            print("Warning unable to place mob num %i with base position; x=%i and y=%i" % (i, basePos))
                            return

                    if not self.mobPresent(newPos):
                        break

            self.mobs.append(testMob)

    def get(self, x, y):
        try:
            return self.tiles[x][y]
        except:
            return False
