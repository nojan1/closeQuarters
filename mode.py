# mode.py: Base class for modes
# A mode is a self contained entity which can be made running by the core and it will then recieve events and instructions for when to draw and such. 
# Author: Niklas Hedlund

class Mode(object):
    def __init__(self, core, fps = 50):
        #Target fps
        self.fps = fps
        self.core = core

    #Called when pygame recieves a event the core doesn't handle
    def handleEvent(self, event, core, numTicks):
        pass

    #Called before the core exits
    def onQuit(self):
        return True

    #Called when this mode is switched out
    def onSwitchOut(self, core):
        pass

    #Called when this mode is switched in
    def onSwitchIn(self, core):
        pass

    #Called before the draw occurs, but still in the same loop itteration as the draw
    def onPreDraw(self, core, numTicks):
        pass

    #Called on separate itteration off the game loop from the draw, might be called multiple times
    def onComputations(self, core, numTicks):
        pass

    #Called on draw
    def onDraw(self, screen, core, numTicks):
        pass
