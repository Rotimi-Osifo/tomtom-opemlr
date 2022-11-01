import constant_data as cData

class Line:
    def __init__(self):
        self.startNodeId = None
        self.endNodeId = None
        self.geometry = None
        self.highway = None
        self.nodes = dict() # only 2 nodes when using a graph
        self.roadId = None
        self.length = None
        self.frc = None
        self.fow = None
        self.direction = None
        self.incominglineid = None

    def setStartNodeId(self, startNodeId):
        self.startNodeId = startNodeId

    def setincominglineid(self, incominglineid):
        self.incominglineid = incominglineid

    def setEndNodeId(self, endNodeId):
        self.endNodeId = endNodeId

    def setGeometry(self, geometry):
        self.geometry = geometry
    
    def addNode(self,  node, nodeId):
        self.nodes[nodeId] = node
    
    def setHighway(self, highway):
        self.highway = highway
    
    def setRoadId(self, roadId):
        self.roadId = roadId
    
    def setLength(self, length):
        self.length = length
    
    def setFrc(self, highway):
        self.frc = int(cData.highway_frc_mapping.get(highway, 0)) #deafult case 0
    
    def setFow(self, highway):
        self.fow = int(cData.highway_fow_mapping.get(highway, 7)) #deafult case 7
    
    def setDirection(self, direction):
        self.direction = direction
        



