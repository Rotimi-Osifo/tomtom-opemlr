class Lines:
    def __init__(self):
        self.lines = dict()
    
    def addLine(self, lineId, line):
        self.lines[lineId] = line
