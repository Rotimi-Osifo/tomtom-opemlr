class trajectorydata:
    def __init__(self, roadid: int, lanedirection: int, mapfilename: str, ref: str, endroadid: int):
        self.roadid = roadid
        self.lanedirection = lanedirection
        self.mapfilename = mapfilename
        self.ref = ref
        self.endroadid = endroadid

    # def __init__(self, roadid, lanedirection):
    #     self.roadid = roadid
    #     self.lanedirection = lanedirection
    #     self.mapfilename = None

