import startdata
class startdatacreator:

    def getstartdata(self):
        startdatalist = list()

        startdatalistloc = startdata.Startdata(4040302, 1)
        startdatalist.append(startdatalistloc)
        startdatalistloc = startdata.Startdata(284402024, 2)
        startdatalist.append(startdatalistloc)
        startdatalistloc = startdata.Startdata(237772646, 1)
        startdatalist.append(startdatalistloc)
        startdatalistloc = startdata.Startdata(237772647, 2)
        startdatalist.append(startdatalistloc)

        return startdatalist

