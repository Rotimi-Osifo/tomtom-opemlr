class Lines:
    def __init__(self):
        self.lines = dict()
    
    def addLine(self, lineId, line):
        self.lines[lineId] = line

    def printlines(self):
        for key in self.lines.keys():
            line = self.lines[key]
            line.printline()
