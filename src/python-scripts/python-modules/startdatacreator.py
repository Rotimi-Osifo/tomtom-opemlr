import startdata
class startdatacreator:

    def getstartdata(self):
        startdatalist = list()

        startdatalistloc = startdata.startdata(4040302, 1)
        startdatalist.append(startdatalistloc)
        startdatalistloc = startdata.startdata(284402024, 2)
        startdatalist.append(startdatalistloc)
        startdatalistloc = startdata.startdata(237772646, 1)
        startdatalist.append(startdatalistloc)
        startdatalistloc = startdata.startdata(237772647, 2)
        startdatalist.append(startdatalistloc)

        return startdatalist

