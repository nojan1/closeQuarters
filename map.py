import os
import random

from tile import *
from config import *
from zombie import *
from textureset import *
from ai import AI

class Map(object):
    def __init__(self):
        self.tiles = None
        self.mobs = []

    def loadLevel(self, levelID):
        ai = AI()
        self.tiles = []
        
        tileTextures = TextureSet("tiles.png")

        path = os.path.join(LEVELPATH, str(levelID)+".lvl")
        if not os.path.exists(path):
            raise Exception("No such levelfile;", path)

        for yPos,line in enumerate(open(path, "r")):
            x = []
            for xPos, char in enumerate(line.strip()):
                pos = (xPos, yPos)
                if char == "." or char == " ":
                    x.append(Empty(pos, tileTextures))
                elif char == "#":
                    x.append(Floor(pos, tileTextures))
                elif char == "W":
                    x.append(Wall(pos, tileTextures))
                elif char == "Z":
                    #Group of mobs, how many depends on dificulty
                    self.allocateMobs(pos, 3, Zombie, ai)
                    
                    #Fill in blank with floor
                    x.append(Floor(pos, tileTextures))
                else:
                    print("Warning: Unknown tile; ", char)

            self.tiles.append(x)
            
    def updateMobs(self, game):
        for m in self.mobs:
            if m.getRect().colliderect(game.getView()):
                m.onActivation(game)

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

    def findTileFromPos(self, pos):
        for y in self.tiles:
            for tile in y:
                if tile.getRect().collidepoint(pos):
                    return tile

        return None

    def mobWasHit(self, mobHitted, weapon):
        if mobHitted.takeDamage(weapon.damage):
            self.mobs.remove(mobHitted)

    def mobPresent(self, pos):
        for m in self.mobs:
            if m.pos == pos:
                return True
        
        return False

    def allocateMobs(self, tileCoords, numMobs, mobClass, ai):
        basePos = (tileCoords[0] * TILESIZE[0], tileCoords[1] * TILESIZE[1])

        posDirs = [(0,-1), (1,0), (0,1), (-1,0)]
        random.shuffle(posDirs)

        for i in range(numMobs):
            testMob = mobClass(basePos, ai)
            if self.mobPresent(basePos):
                #Find new pos
                addedDistance = 0
                while 1:
                    addedDistance += testMob.getRect().width
                    newPos = (basePos[0] + (posDirs[0][0] * addedDistance), basePos[1] + (posDirs[0][1] * addedDistance))
                    testMob = mobClass(newPos, ai)
                
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
