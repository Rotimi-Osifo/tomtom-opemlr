class EnrichedCoordinate:
    def __init__(self, coord, dist):
        self.lat = coord[1]
        self.long = coord[0]
        self.dist = dist