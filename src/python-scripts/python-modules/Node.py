class Node:
    def __init__(self):
        self.roadId = None
        self.nodeId = None
        self.coordinate = None
        self.nodeLink = None
    
    def setRoadId(self, roadId):
        self.roadId = roadId
    
    def setNodeId(self, nodeId):
        self.nodeId = nodeId
    
    def setCoordinate(self, coordinate):
        self.coordinate = coordinate
    
    def setnodeLink(self, nodeId):
        self.nodeLink =  "node-"+ str(nodeId)