import Nodes
import constant_data as cData
class segment:
    def __init__(self):
        self.start = None
        self.end = None
        self.cumDist = None
        self.maxspeed = None
        self.id = None
        self.travel_time = None
        self.incoming = None
        self.outgoing = None
        self.geometry = None
        self.lastv = None
        self.firstu = None
        self.length = None
        self.nodes: Nodes.Nodes = None
        self.nodeslist = list()
        self.direction = None
        self.frc = None
        self.fow = None

    def setFrc(self, highway):
        self.frc = int(cData.highway_frc_mapping.get(highway, 0))  # deafult case 0

    def setFow(self, highway):
        self.fow = int(cData.highway_fow_mapping.get(highway, 7))  # deafult case 7

    def printsegment(self):
        print("segment id -:, ", self.id, ", start node -:, ", self.start, ", end -: ", self.end)
        for node in self.nodeslist:
            node.printnode()