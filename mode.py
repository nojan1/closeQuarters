class Mode(object):
    def __init__(self, core, fps = 50):
        self.fps = fps
        self.core = core

    def handleEvent(self, event, core, numTicks):
        pass

    def onQuit(self):
        return True

    def onPreDraw(self, core, numTicks):
        pass

    def onComputations(self, core, numTicks):
        pass

    def onDraw(self, screen, core):
        pass
