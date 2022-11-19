import segment
import graphprocessor
#import utilities

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
        startdataloc = startdata.Startdata(4040443, 2, "map_data_as_geojson_" + str(4040443))
        self.startdatalist.append(startdataloc)
        startdataloc = startdata.Startdata(222217364, 2, "map_data_as_geojson_" + str(222217364))
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

    # def __buildconnectedsegments(self, segments_, startid, lanedirection):
    #     if self.visitedset.count(startid) == 0:
    #         try:
    #             seg:segment.segment = segments_[startid]
    #             seg.direction = lanedirection
    #             segments_[startid] = seg  # updating with direction
    #             self.visitedset.append(startid)
    #             outgoing:int = utilities.getfirstlementfromlist(seg.outgoing)
    #             if outgoing is not None:
    #                 self.__buildconnectedsegments(segments_, outgoing, lanedirection)
    #             else:
    #                 return self.visitedset
    #         except KeyError:
    #             print("the key-: ", startid, " is not in the dictionary!")
    #     else:
    #         return self.visitedset

    def __buildconnectedsegmentsext(self, segments_, startid, lanedirection):
        if self.visitedset.count(startid) == 0:
            try:
                seg:segment.segment = segments_[startid]
                incomingids: list = seg.incoming
                if len(incomingids) >= 1:
                    for incomingid in incomingids:
                        if incomingid is not None:
                            segincoming:segment.segment = segments_[incomingid]
                            if self.visitedset.count(incomingid) == 0:
                                segincoming.direction = lanedirection
                                segments_[incomingid] = segincoming
                                self.visitedset.append(incomingid)

                seg.direction = lanedirection
                segments_[startid] = seg  # updating with direction
                self.visitedset.append(startid)

                outgoingids: list = seg.outgoing
                if len(outgoingids) >= 1:
                    for outgoingid in outgoingids:
                        if outgoingid is not None:
                            if self.visitedset.count(outgoingid) == 0:
                                self.__buildconnectedsegmentsext(segments_, outgoingid, lanedirection)
                else:
                    return self.visitedset
            except KeyError:
                print("the key-: ", startid, " is not in the dictionary!")
        else:
            return self.visitedset



    def buildconnectedsegments(self, graphnetwork):

        segment_processor = graphprocessor.graphprocessor()
        segment_processor.preprocess(graphnetwork)
        self.segments = segment_processor.preprocessed_segments
        self.__getstartdata()
        for startdataloc in self.startdatalist:
            self.visitedset = list()
            self.__buildconnectedsegmentsext(self.segments, startdataloc.roadid, startdataloc.lanedirection)
            print(self.visitedset)
            self.datastore[startdataloc.roadid] = self.visitedset

