class Mode(object):
    def __init__(self, core, fps = 50):
        self.fps = fps
        self.core = core

    def handleEvent(self, event, core, numTicks):
        pass

    def onQuit(self):
        return True

    def onPreEventCheck(self, core, numTicks):
        pass

    def onPostEventCheck(self, core, numTicks):
        pass

    def onDraw(self, screen, core):
        pass
