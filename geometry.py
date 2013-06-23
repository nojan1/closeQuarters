
def worldToScreen(worldPos, screenView):
    x = worldPos[0] - screenView.x
    y = worldPos[1] - screenView.y

    return (x, y)

def screenToWorld(screenPos, screenView):
    pass
    
