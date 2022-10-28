
class LineData:
    def __init__(self):
        self.currentSegmentId = None
        self.connectedSegmentId = None
        self.connectedSegmentIsBefore = None
        self.currentSegmentIsBefore = None
        self.connectionPoint = None
    
    def setCurrentSegmentId(self, currentSegmentId):
        self.currentSegmentId = currentSegmentId
     
    def setConnectedSegmentId(self, connectedSegmentId):
        self.connectedSegmentId = connectedSegmentId
    
    def setConnectedSegmentIsBefore(self, connectedSegmentIsBefore):
        self.connectedSegmentIsBefore = connectedSegmentIsBefore
    
    def setCurrentSegmentIsBefore(self, currentSegmentIsBefore):
        self.currentSegmentIsBefore = currentSegmentIsBefore

    def setConnectionPoint(self, connectionPoint):
        self.connectionPoint = connectionPoint

class ConnectedLinesData:
    def __init__(self):
        self.linesData = list()
    
    def addToLinesData(self, lineData):
        self.linesData.append(lineData)