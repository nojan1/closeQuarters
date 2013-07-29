from mode import *
from pygame import *

class InstructionsScreen(Mode):
    def __init__(self, core):
        Mode.__init__(self, core, 30)

        self.fontHeader = font.Font(None, 70)
        self.fontContent = font.Font(None, 40)

        self.text = """The purpose of the game is to move through corridors and kill mobs

The controls are WASD for movement and the mouse for targeting, a
green circle drawn around the player will show the target angle.

New weapons and more health are available through pickups, once
a weapon has been depleted the previous one will be used. 
The first weapon is a pistol with unlimited ammo.

Press ESCAPE to return to menu""" 
    
    def onDraw(self, screen, core, numTicks):
        screen.fill((0,0,0))

        topic = self.fontHeader.render("Instructions", True, (255,255,255))
        screen.blit(topic, (40,40))
        
        x,y = (50, 100)
        for line in self.text.split("\n"):
            rendered = self.fontContent.render(line, True, (255,255,255))
            screen.blit(rendered, (x,y))
            y += rendered.get_height()

    def handleEvent(self, event, core, numTicks):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                core.revertLastMode()
