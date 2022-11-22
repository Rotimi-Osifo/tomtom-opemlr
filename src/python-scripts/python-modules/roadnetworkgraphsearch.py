import segment
import graphprocessor
import graphfunctions

import startdata
class roadnetworkgraphsearch:
    def __init__(self):
        self.visitedset = None
        self.datastore = dict()
        self.trajectorydistances = dict()
        self.postprocessed_segments = dict()
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

    def __calculatedistances(self, segments_, startid: int, distance: float):
        try:
            seg: segment.segment = segments_[startid]
            prevdistance = distance
            distance = prevdistance + (seg.length)
            seg.cumDist = distance
            segments_[startid] = seg
            outgoingids: list = seg.outgoing

            print("distances - current segment-: ", startid, ", segment-: ", seg.length, ", start-: ", seg.cumDist)
            if len(outgoingids) == 2:
                reset: float = 0.0
                for outgoingid in outgoingids:
                    if outgoingid is not None:
                        distance = distance - reset
                        print("distance-: ", distance, " reset-: ", reset, "id-:, ", outgoingid)
                        self.__calculatedistances(segments_, outgoingid, distance)
                        print("distance-: ", distance, " reset-: ", reset, "id-:, ", outgoingid)
            if len(outgoingids) == 1:
                outgoingid = outgoingids[0]
                if outgoingid is not None:
                    self.__calculatedistances(segments_, outgoingid, distance)

        except KeyError:
            print("the key-: ", startid, " is not in the dictionary!")

    def __buildconnectedsegmentsext(self, segments_, startid, lanedirection):

        if self.visitedset.count(startid) == 0:
            try:
                seg:segment.segment = segments_[startid]
                incomingids: list = seg.incoming
                if len(incomingids) == 1:
                    incomingid = incomingids[0]
                    if incomingid is not None:
                        if self.visitedset.count(incomingid) == 0:
                            seg.direction = lanedirection
                            seg.incoming = [incomingid]
                            segments_[startid] = seg
                            self.visitedset.append(incomingid)
                        else:
                            seg.direction = lanedirection
                            segments_[startid] = seg
                    else:
                        seg.direction = lanedirection
                        segments_[startid] = seg


                elif len(incomingids) == 2:
                    firstincomingincomingseg: segment.segment = segments_[incomingids[0]]
                    print("Trace back-: ", startid, ", ", incomingids[0], " ", firstincomingincomingseg.cumDist)

                    secondincomingincomingseg: segment.segment = segments_[incomingids[1]]
                    print("Trace back-: ", startid, ", ", incomingids[1], " ", secondincomingincomingseg.cumDist)
                    incomingidloc: int = None
                    if firstincomingincomingseg.cumDist > secondincomingincomingseg.cumDist:
                        incomingidloc = incomingids[0]
                    else:
                        incomingidloc = incomingids[1]

                    print("After trace back-: ", startid, ", ", incomingidloc)
                    if incomingidloc is not None:
                        if self.visitedset.count(incomingidloc) == 0:
                            seg.direction = lanedirection
                            seg.incoming = [incomingidloc]
                            self.visitedset.append(incomingidloc)
                    else:
                        seg.direction = lanedirection
                        segments_[startid] = seg
                else:
                    seg.direction = lanedirection
                    segments_[startid] = seg

                #seg.direction = lanedirection
                #self.postprocessed_segments[startid] = seg  # updating with direction
                if self.visitedset.count(startid) == 0:
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

    def __createconnectedsegmentsext(self, segments_, startid, lanedirection, trajectorylength: float):

        if self.visitedset.count(startid) == 0:
            try:
                seg:segment.segment = segments_[startid]
                incomingids: list = seg.incoming
                if len(incomingids) == 1:
                    incomingid = incomingids[0]
                    if incomingid is not None:
                        if self.visitedset.count(incomingid) == 0:
                            seg.direction = lanedirection
                            seg.incoming = [incomingid]
                            segments_[startid] = seg
                            self.visitedset.append(incomingid)
                        else:
                            seg.direction = lanedirection
                            segments_[startid] = seg
                    else:
                        seg.direction = lanedirection
                        segments_[startid] = seg


                elif len(incomingids) == 2:
                    firstincomingincomingseg: segment.segment = segments_[incomingids[0]]
                    print("Trace back-: ", startid, ", ", incomingids[0], " ", firstincomingincomingseg.cumDist)

                    secondincomingincomingseg: segment.segment = segments_[incomingids[1]]
                    print("Trace back-: ", startid, ", ", incomingids[1], " ", secondincomingincomingseg.cumDist)
                    incomingidloc: int = None
                    if firstincomingincomingseg.cumDist > secondincomingincomingseg.cumDist:
                        incomingidloc = incomingids[0]
                    else:
                        incomingidloc = incomingids[1]

                    print("After trace back-: ", startid, ", ", incomingidloc)
                    if incomingidloc is not None:
                        if self.visitedset.count(incomingidloc) == 0:
                            seg.direction = lanedirection
                            seg.incoming = [incomingidloc]
                            self.visitedset.append(incomingidloc)
                    else:
                        seg.direction = lanedirection
                        segments_[startid] = seg
                else:
                    seg.direction = lanedirection
                    segments_[startid] = seg

                #seg.direction = lanedirection
                #self.postprocessed_segments[startid] = seg  # updating with direction
                if self.visitedset.count(startid) == 0:
                    self.visitedset.append(startid)

                outgoingids: list = seg.outgoing
                if len(outgoingids) == 1:
                    outgoingid = outgoingids[0]
                    if outgoingid is not None:
                        if self.visitedset.count(outgoingid) == 0:
                            seglic: segment.segment = segments_[startid]
                            self.__createconnectedsegmentsext(segments_, outgoingid, lanedirection, trajectorylength)
                if len(outgoingids) == 2:
                    firstsegloc: segment.segment = segments_[outgoingids[0]]
                    secondsegloc: segment.segment = segments_[outgoingids[1]]
                    firstremainingdistance = trajectorylength - (firstsegloc.cumDist)
                    secondremainingdistance = trajectorylength - (secondsegloc.cumDist)
                    if secondremainingdistance > firstremainingdistance:
                        if self.visitedset.count(outgoingids[1]) == 0:
                            seg.outgoing = [outgoingids[1]]
                            segments_[startid] = seg
                            self.__createconnectedsegmentsext(segments_, outgoingids[1], lanedirection, trajectorylength)
                    else:
                        if self.visitedset.count(outgoingids[0]) == 0:
                            seg.outgoing = [outgoingids[0]]
                            segments_[startid] = seg
                            self.__createconnectedsegmentsext(segments_, outgoingids[0], lanedirection, trajectorylength)


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

            distance:float = 0
            self.__calculatedistances(self.segments, startdataloc.roadid, distance)
            self.trajectorydistances[startdataloc.roadid] = distance

            self.visitedset = list()
            #self.__buildconnectedsegmentsext(self.segments, startdataloc.roadid, startdataloc.lanedirection)
            self.__createconnectedsegmentsext(self.segments, startdataloc.roadid, startdataloc.lanedirection, distance)
            print(self.visitedset)
            self.datastore[startdataloc.roadid] = self.visitedset

