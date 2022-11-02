import GeometryData as gData

class Nodes:
    def __init__(self):
        self.nodes = dict()

    def addToNodes(self, node, networkid):
        self.nodes[networkid] = node

    def printnodes(self):
        print("printing nodes")
        for key in self.nodes.keys():
            segmentnodes = self.nodes[key]
            print("printing nodes for -:", key)
            for node in segmentnodes:
                node.printnode()

    def hassamecoords(self, currentnode, prevnode):
        if prevnode is None:
            return False
        else:
            currentcoord = currentnode.coordinate
            prevcoord = prevnode.coordinate
            geometrydata = gData.GeometryData()

            return geometrydata.pointsAreEqual(currentcoord, prevcoord)