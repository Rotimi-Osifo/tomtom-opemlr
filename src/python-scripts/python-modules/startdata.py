class Startdata:
    def __init__(self, roadid, lanedirection):
        self.roadid = roadid
        self.lanedirection = lanedirection
    def getstartdata(self):
        startdatalist = list()

        startdatalistloc = Startdata.startdata(4040302, 1)
        startdatalist.append(startdatalistloc)
        startdatalistloc = Startdata.startdata(284402024, 2)
        startdatalist.append(startdatalistloc)
        startdatalistloc = Startdata.startdata(237772646, 1)
        startdatalist.append(startdatalistloc)
        startdatalistloc = Startdata.startdata(237772647, 2)
        startdatalist.append(startdatalistloc)

        return startdatalist