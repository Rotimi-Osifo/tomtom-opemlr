
class trajectory:

    def __init__(self, startid:int, endid:int, direction:int, highwayref:str, name: str):
        self.startsegmentid = startid
        self.endsegmentid = endid
        self.direction = direction
        self.highwayref = highwayref
        self.name = name # for example street name
        self.path: list = None
