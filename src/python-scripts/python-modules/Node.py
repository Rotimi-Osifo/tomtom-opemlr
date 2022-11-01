class Node:
    def __init__(self):
        self.roadId = None
        self.nodeId = None
        self.coordinate = None
        self.name = None
    
    def setRoadId(self, roadId):
        self.roadId = roadId
    
    def setNodeId(self, nodeId):
        self.nodeId = nodeId
    
    def setCoordinate(self, coordinate):
        self.coordinate = coordinate
    
    def setnodename(self, roadId):
        self.name =  "node-"+ str(roadId)