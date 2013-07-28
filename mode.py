# mode.py: Base class for modes
# A mode is a self contained entity which can be made running by the core and it will then recieve events and instructions for when to draw and such. 
# Author: Niklas Hedlund

class Mode(object):
    def __init__(self, core, fps = 50):
        self.fps = fps
        self.core = core

    def handleEvent(self, event, core, numTicks):
        pass

    def onQuit(self):
        return True

    def onSwitchOut(self, core):
        pass

    def onSwitchIn(self, core):
        pass

    def onPreDraw(self, core, numTicks):
        pass

    def onComputations(self, core, numTicks):
        pass

    def onDraw(self, screen, core, numTicks):
        pass
