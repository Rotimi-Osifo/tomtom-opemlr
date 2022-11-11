import barefootoutput

class barefootdatamanager:
    def __init__(self):
        self.coordinates = barefootoutput.coordinates


    def createbarefootoutputroad(self):
        barefootroadsegments = list()
        for segmenttupples in self.coordinates:
            for point in segmenttupples:
                barefootroadsegments.append((point[1], point[0]))
        return barefootroadsegments