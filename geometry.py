
def worldToScreen(worldPos, screenView):
    #if screenView.collidepoint(worldPos):
        #return worldPos

    x = worldPos[0] - screenView.x
    y = worldPos[1] - screenView.y

    return (x, y)

def screenToWorld(screenPos, screenView):
    pass

def getAngleDistance(source, destination):
    x1, y1 = source
    x2, y2 = destination

    dX = x1 - x2
    dY = y1 - y2

    angle = math.atan2(dY * -1, dX * -1)
    distance = math.sqrt((dX*dX) + (dY*dY))
        
    return (angle, distance)
    
