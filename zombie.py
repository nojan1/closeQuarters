from sprite import *

class Zombie(nSprite):
    def __init__(self, pos):
        nSprite.__init__(self)
        self.pos = pos
        self.size = (20,20)

    def draw(self, screen, game):
        rectScreen = self.getRectScreen(game)

        #Draw mob
        screen.fill((100,0,200), rectScreen)

    def takeDamage(self, damage):
        #True = Dead, False = "Took it like a man"
        return True
