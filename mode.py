class Mode(object):
    def __init__(self, core, fps = 50):
        self.fps = fps
        self.core = core

    def handleEvent(self, event, core):
        pass

    def onQuit(self):
        return True

    def onPreEventCheck(self, core):
        pass

    def onPostEventCheck(self, core):
        pass

    def onDraw(self, screen, core):
        pass
