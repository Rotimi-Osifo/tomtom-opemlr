import segment
import segmentinitializer

import startdata
class roadnetworkgraphsearch:
    def __init__(self):
        self.visitedset = None #list()
        self.datastore = dict()
        self.segments = None


    def __getstartdata(self):
        startdatalist = list()

        startdatalistloc = startdata.Startdata(4040302, 1)
        startdatalist.append(startdatalistloc)
        #startdatalistloc = startdata.Startdata(284402024, 2)
        #startdatalist.append(startdatalistloc)
        #startdatalistloc = startdata.Startdata(237772646, 1)
        #startdatalist.append(startdatalistloc)
        #startdatalistloc = startdata.Startdata(237772647, 2)
        #startdatalist.append(startdatalistloc)

        return startdatalist

    def __buildconnectedsegments(self, segments_, startid, lanedirection):
        if self.visitedset.count(startid) == 0:
            self.visitedset.append(startid)
            seg:segment.segment = segments_[startid]
            seg.direction = lanedirection
            segments_[startid] = seg #updateing with direction
            if seg.outgoing is not None:
                self.__buildconnectedsegments(segments_, seg.outgoing, lanedirection)
            else:
                return self.visitedset
        else:
            return self.visitedset

    def buildconnectedsegments(self, graphnetwork):

        segment_initializer = segmentinitializer.segmentinitializer()
        segment_initializer.initialize_segments(graphnetwork)
        self.segments = segment_initializer.initialized_segments
        startdatalist = self.__getstartdata()
        for startdataloc in startdatalist:
            self.visitedset = list()
            self.__buildconnectedsegments(self.segments, startdataloc.roadid, startdataloc.lanedirection)
            print(self.visitedset)
            self.datastore[startdataloc.roadid] = self.visitedset

