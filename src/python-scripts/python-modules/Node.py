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

    def printnode(self):
        print("printing node")
        print(self.roadId, " ", self.nodeId, " [", self.coordinate[0], ",", self.coordinate[1], "]")