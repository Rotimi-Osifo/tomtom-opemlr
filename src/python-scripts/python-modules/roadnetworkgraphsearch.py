import segment
import segmentinitializer

import startdata
class roadnetworkgraphsearch:
    def __init__(self):
        self.visitedset = None #list()
        self.datastore = dict()
        self.segments = None
        self.startdatalist = None


    def __getstartdata(self):
        self.startdatalist = list()

        startdataloc = startdata.Startdata(4040302, 1, "map_data_as_geojson_" + str(4040302))
        self.startdatalist.append(startdataloc)
        startdataloc = startdata.Startdata(284402024, 2, "map_data_as_geojson_" + str(284402024))
        self.startdatalist.append(startdataloc)
        startdataloc = startdata.Startdata(237772646, 1, "map_data_as_geojson_" + str(237772646))
        self.startdatalist.append(startdataloc)
        startdataloc = startdata.Startdata(237772647, 2, "map_data_as_geojson_" + str(237772647))
        self.startdatalist.append(startdataloc)

        return self.startdatalist

    def __buildconnectedsegments(self, segments_, startid, lanedirection):
        if self.visitedset.count(startid) == 0:
            self.visitedset.append(startid)
            seg:segment.segment = segments_[startid]
            seg.direction = lanedirection
            segments_[startid] = seg #updating with direction
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
        self.__getstartdata()
        for startdataloc in self.startdatalist:
            self.visitedset = list()
            self.__buildconnectedsegments(self.segments, startdataloc.roadid, startdataloc.lanedirection)
            print(self.visitedset)
            self.datastore[startdataloc.roadid] = self.visitedset

