import GeometryData as gData

class Nodes:
    def __init__(self):
        self.nodes = dict()
        self.nodeslist = list()

    def addToNodes(self, node, roadid):
        self.nodes[roadid] = node

    def addToNodesList(self, node):
        self.nodeslist.append(node)

    def printnodes(self):
        print("printing nodes")
        for key in self.nodes.keys():
            segmentnodes = self.nodes[key]
            print("printing nodes for -:", key)
            for node in segmentnodes:
                node.printnode()
