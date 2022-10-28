class ConnectedSegments:
    def __init__(self):
        self.unsortedConnectedSegments = dict()
        self.sortedConnectedSegments = list()
     
    def addToUnsortedConnectedLines(self, roadNetwork):
        for road in roadNetwork.itertuples():
            self.unsortedConnectedSegments[road.id] = road.geometry

    def addToSortedConnectedLines(self, roadId):
        self.sortedConnectedSegments.append(int(roadId))  