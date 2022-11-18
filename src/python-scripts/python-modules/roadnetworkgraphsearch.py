import segment
import segmentinitializer

import startdata
class roadnetworkgraphsearch:
    def __init__(self):
        self.visitedset = None
        self.datastore = dict()
        self.segments = None
        self.startdatalist = None


    def __getstartdata(self):
        self.startdatalist = list()

        startdataloc = startdata.Startdata(4040302, 1, "map_data_as_geojson_" + str(4040302))
        self.startdatalist.append(startdataloc)
        startdataloc = startdata.Startdata(408861785, 2, "map_data_as_geojson_" + str(408861785))
        self.startdatalist.append(startdataloc)
        startdataloc = startdata.Startdata(39887921, 2, "map_data_as_geojson_" + str(39887921))
        self.startdatalist.append(startdataloc)
        startdataloc = startdata.Startdata(237772646, 1, "map_data_as_geojson_" + str(237772646))
        self.startdatalist.append(startdataloc)
        startdataloc = startdata.Startdata(117090882, 2, "map_data_as_geojson_" + str(117090882))
        self.startdatalist.append(startdataloc)
        startdataloc = startdata.Startdata(10275796, 1, "map_data_as_geojson_" + str(10275796))
        self.startdatalist.append(startdataloc)
        startdataloc = startdata.Startdata(297042452, 2, "map_data_as_geojson_" + str(297042452))
        self.startdatalist.append(startdataloc)
        startdataloc = startdata.Startdata(4040439, 2, "map_data_as_geojson_" + str(4040439))
        self.startdatalist.append(startdataloc)

        return self.startdatalist

    def __buildconnectedsegments(self, segments_, startid, lanedirection):
        if self.visitedset.count(startid) == 0:
            try:
                seg:segment.segment = segments_[startid]
                seg.direction = lanedirection
                segments_[startid] = seg  # updating with direction
                self.visitedset.append(startid)
                if seg.outgoing is not None:
                    self.__buildconnectedsegments(segments_, seg.outgoing, lanedirection)
                else:
                    return self.visitedset
            except KeyError:
                print("the key-: ", startid, " is not in the dictionary!")
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

