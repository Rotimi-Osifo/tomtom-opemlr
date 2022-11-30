import segment
import graphprocessor


import trajectorydata
import connectedsegments
import FeatureCollectionData as fcData


class roadnetworkgraphsearch:
    def __init__(self):
        self.visitedset = None
        self.datastore = dict()
        self.trajectoriesstore = dict()
        self.trajectorydistances = dict()
        self.postprocessed_segments = dict()
        self.segments = dict()
        self.trajectorydatalist = None

    def __getstartdata(self) -> dict:
        self.trajectorydatalist = dict()

        trajectorydataloc = trajectorydata.trajectorydata(4040302, 1, "map_data_as_geojson_" + str(4040302), "E 6",
                                                     168975966)
        self.trajectorydatalist[4040302] = trajectorydataloc
        trajectorydataloc = trajectorydata.trajectorydata(4040443, 2, "map_data_as_geojson_" + str(4040443), "E 6",
                                                      284402024)
        self.trajectorydatalist[4040443] = trajectorydataloc
        trajectorydataloc = trajectorydata.trajectorydata(237772646, 1, "map_data_as_geojson_" + str(237772646), "E 45",
                                                      1023578391)
        self.trajectorydatalist[237772646] = trajectorydataloc
        trajectorydataloc = trajectorydata.trajectorydata(117090882, 2, "map_data_as_geojson_" + str(117090882), "E 45",
                                                      237772647)
        self.trajectorydatalist[117090882] = trajectorydataloc
        trajectorydataloc = trajectorydata.trajectorydata(10275796, 1, "map_data_as_geojson_" + str(10275796), "E 20",
                                                      4040484)
        self.trajectorydatalist[10275796] = trajectorydataloc
        trajectorydataloc = trajectorydata.trajectorydata(4040439, 2, "map_data_as_geojson_" + str(4040439), "E 20",
                                                     297042452)
        self.trajectorydatalist[4040439] = trajectorydataloc

        return self.trajectorydatalist

    def __calculatedistances(self, segments_, startid: int, distance: float):
        try:
            seg: segment.segment = segments_[startid]
            prevdistance = distance
            distance = prevdistance + (seg.length)
            seg.cumDist = distance
            segments_[startid] = seg
            outgoingids: list = seg.successors

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
                seg: segment.segment = segments_[startid]
                predecessorids: list = seg.predecessors
                if len(predecessorids) == 1:
                    predecessorid = predecessorids[0]
                    if predecessorid is not None:
                        if self.visitedset.count(predecessorid) == 0:
                            seg.direction = lanedirection
                            seg.predecessors = [predecessorid]
                            segments_[startid] = seg
                            self.visitedset.append(predecessorid)
                        else:
                            seg.direction = lanedirection
                            segments_[startid] = seg
                    else:
                        seg.direction = lanedirection
                        segments_[startid] = seg


                elif len(predecessorids) == 2:
                    firstpredecessorseg: segment.segment = segments_[predecessorids[0]]
                    print("Trace back-: ", startid, ", ", predecessorids[0], " ", firstpredecessorseg.cumDist)

                    secondpredecessorseg: segment.segment = segments_[predecessorids[1]]
                    print("Trace back-: ", startid, ", ", predecessorids[1], " ", secondpredecessorseg.cumDist)
                    predecessoridloc: int = None
                    if firstpredecessorseg.cumDist > secondpredecessorseg.cumDist:
                        predecessoridloc = predecessorids[0]
                    else:
                        predecessoridloc = predecessorids[1]

                    print("After trace back-: ", startid, ", ", predecessoridloc)
                    if predecessoridloc is not None:
                        if self.visitedset.count(predecessoridloc) == 0:
                            seg.direction = lanedirection
                            seg.predecessors = [predecessoridloc]
                            self.visitedset.append(predecessoridloc)
                    else:
                        seg.direction = lanedirection
                        segments_[startid] = seg
                else:
                    seg.direction = lanedirection
                    segments_[startid] = seg

                # seg.direction = lanedirection
                # self.postprocessed_segments[startid] = seg  # updating with direction
                if self.visitedset.count(startid) == 0:
                    seg.direction = lanedirection
                    segments_[startid] = seg
                    self.visitedset.append(startid)

                successorids: list = seg.successors
                if len(successorids) >= 1:
                    for successorid in successorids:
                        if successorid is not None:
                            if self.visitedset.count(successorid) == 0:
                                self.__buildconnectedsegmentsext(segments_, successorid, lanedirection)
                else:
                    return self.visitedset
            except KeyError:
                print("the key-: ", startid, " is not in the dictionary!")
        else:
            return self.visitedset

    def __buildconnectedsegmentsext2(self, segments_: dict, startid: int, lanedirection: int, endid: int):

        if self.visitedset.count(startid) == 0:
            try:
                seg: segment.segment = segments_[startid]
                predecessorids: list = seg.predecessors
                if len(predecessorids) == 1:
                    predecessorid = predecessorids[0]
                    if predecessorid is not None:
                        if self.visitedset.count(predecessorid) == 0:
                            seg.direction = lanedirection
                            seg.predecessors = [predecessorid]
                            segments_[startid] = seg
                            self.visitedset.append(predecessorid)
                        else:
                            seg.direction = lanedirection
                            segments_[startid] = seg
                    else:
                        seg.direction = lanedirection
                        segments_[startid] = seg


                elif len(predecessorids) == 2:
                    firstpredecessorseg: segment.segment = segments_[predecessorids[0]]
                    print("Trace back-: ", startid, ", ", predecessorids[0], " ", firstpredecessorseg.cumDist)

                    secondpredecessorseg: segment.segment = segments_[predecessorids[1]]
                    print("Trace back-: ", startid, ", ", predecessorids[1], " ", secondpredecessorseg.cumDist)
                    predecessoridloc: int = None
                    if firstpredecessorseg.cumDist > secondpredecessorseg.cumDist:
                        predecessoridloc = predecessorids[0]
                    else:
                        predecessoridloc = predecessorids[1]

                    print("After trace back-: ", startid, ", ", predecessoridloc)
                    if predecessoridloc is not None:
                        if self.visitedset.count(predecessoridloc) == 0:
                            seg.direction = lanedirection
                            seg.predecessors = [predecessoridloc]
                            self.visitedset.append(predecessoridloc)
                elif predecessorids is None: # start of trajectory - possibly
                    seg.direction = lanedirection
                    segments_[startid] = seg
                    self.visitedset.append(startid)

                successorids: list = seg.successors
                if successorids is None: # possibly end of trajectories
                    seg.direction = lanedirection
                    segments_[startid] = seg
                    # already added to visited list as a successor.
                    # No need to add it again.
                elif len(successorids) == 1:
                    successorid = successorids[0]
                    if self.visitedset.count(successorid) == 0:
                        seg.successors = [successorid]
                        seg.direction = lanedirection
                        segments_[startid] = seg #updated
                        self.visitedset.append(successorid)
                if len(successorids) == 2:
                    successoridfirst = successorids[0]
                    successoridsecond = successorids[1]
                    for successorid in successorids:
                        if successorid is not None:
                            if self.visitedset.count(successorid) == 0:
                                self.__buildconnectedsegmentsext(segments_, successorid, lanedirection)
                else:
                    return self.visitedset
            except KeyError:
                print("the key-: ", startid, " is not in the dictionary!")
        else:
            return self.visitedset

    def __createconnectedsegmentsext(self, segments_, startid, lanedirection, trajectorylength: float):

        if self.visitedset.count(startid) == 0:
            try:
                seg: segment.segment = segments_[startid]
                predecessors: list = seg.predecessors
                if len(predecessors) == 1:
                    predecessorid = predecessors[0]
                    if predecessorid is not None:
                        if self.visitedset.count(predecessorid) == 0:
                            seg.direction = lanedirection
                            seg.predecessors = [predecessorid]
                            segments_[startid] = seg
                            self.visitedset.append(predecessorid)
                        else:
                            seg.direction = lanedirection
                            segments_[startid] = seg
                    else:
                        seg.direction = lanedirection
                        segments_[startid] = seg


                elif len(predecessors) == 2:
                    firstpredecessorseg: segment.segment = segments_[predecessors[0]]
                    print("Trace back-: ", startid, ", ", predecessors[0], " ", firstpredecessorseg.cumDist)

                    secondpredecessorseg: segment.segment = segments_[predecessors[1]]
                    print("Trace back-: ", startid, ", ", predecessors[1], " ", secondpredecessorseg.cumDist)
                    predecessoridloc: int = None
                    if firstpredecessorseg.cumDist > secondpredecessorseg.cumDist:
                        predecessoridloc = predecessors[0]
                    else:
                        predecessoridloc = predecessors[1]

                    print("After trace back-: ", startid, ", ", predecessoridloc)
                    if predecessoridloc is not None:
                        if self.visitedset.count(predecessoridloc) == 0:
                            seg.direction = lanedirection
                            seg.predecessors = [predecessoridloc]
                            self.visitedset.append(predecessoridloc)
                    else:
                        seg.direction = lanedirection
                        segments_[startid] = seg
                else:
                    seg.direction = lanedirection
                    segments_[startid] = seg

                # seg.direction = lanedirection
                # self.postprocessed_segments[startid] = seg  # updating with direction
                if self.visitedset.count(startid) == 0:
                    self.visitedset.append(startid)

                successors: list = seg.successors
                if len(successors) == 1:
                    successorid = successors[0]
                    if successorid is not None:
                        if self.visitedset.count(successorid) == 0:
                            seglic: segment.segment = segments_[startid]
                            self.__createconnectedsegmentsext(segments_, successorid, lanedirection, trajectorylength)
                if len(successors) == 2:
                    firstsegloc: segment.segment = segments_[successors[0]]
                    secondsegloc: segment.segment = segments_[successors[1]]
                    firstremainingdistance = trajectorylength - (firstsegloc.cumDist)
                    secondremainingdistance = trajectorylength - (secondsegloc.cumDist)
                    if secondremainingdistance > firstremainingdistance:
                        if self.visitedset.count(successors[1]) == 0:
                            seg.successors = [successors[1]]
                            segments_[startid] = seg
                            self.__createconnectedsegmentsext(segments_, successors[1], lanedirection, trajectorylength)
                    else:
                        if self.visitedset.count(successors[0]) == 0:
                            seg.successors = [successors[0]]
                            segments_[startid] = seg
                            self.__createconnectedsegmentsext(segments_, successors[0], lanedirection, trajectorylength)


                else:
                    return self.visitedset
            except KeyError:
                print("the key-: ", startid, " is not in the dictionary!")
        else:
            return self.visitedset

    def __createconnectedsegmentsfromgraph(self, segments_: dict, trajectory_path_list: list):
        for trajectory_path_id in trajectory_path_list:
            try:
                seg: segment.segment = segments_[trajectory_path_id]
                predecessors: list = seg.predecessors
                if predecessors is not None:
                    closest = predecessors[0]

            except KeyError:
                print("the key-: ", trajectory_path_id, " is not in the dictionary!")



    def buildconnectedsegments(self, graphnetwork):

        segment_processor = graphprocessor.graphprocessor()
        segment_processor.preprocess(graphnetwork)
        self.segments = segment_processor.preprocessed_segments

        self.__getstartdata()
        for trajectorydataloc in self.trajectorydatalist:
            distance: float = 0
            self.__calculatedistances(self.segments, trajectorydataloc.roadid, distance)
            self.trajectorydistances[trajectorydataloc.roadid] = distance

            self.visitedset = list()
            self.__createconnectedsegmentsext(self.segments, trajectorydataloc.roadid, trajectorydataloc.lanedirection, distance)
            print(self.visitedset)
            self.datastore[trajectorydataloc.roadid] = self.visitedset

    def buildconnectedsegmentsext(self, graphnetwork, trajectory_store_key: int):

        self.__getstartdata()
        trajectorydataloc = self.trajectorydatalist[trajectory_store_key]
        segment_processor = graphprocessor.graphprocessor()
        trajectory_segments = segment_processor.preprocessext(graphnetwork,
                                                              trajectorydataloc.trajectorystart,
                                                              trajectorydataloc.trajectoryend,
                                                              trajectorydataloc.lanedirection
                                                              )

        # self.visitedset = list()
        # self.__createconnectedsegmentsext(trajectory_segments, trajectorydataloc.trajectorystart, trajectorydataloc.lanedirection)
        # print(self.visitedset)

        trajectory_start_segment: segment.segment = trajectory_segments[trajectorydataloc.trajectorystart]
        trajectory_path_list: list = trajectory_start_segment.successors
        trajectory_path_list.insert(0, trajectorydataloc.trajectorystart)

        connected_segments = connectedsegments.connectedsegments()
        re_initialized_trajectory_segments = connected_segments.buildconnectedsegmentsext(trajectory_segments,
                                                                                          trajectory_path_list)

        featurecollectiondata = fcData.FeatureCollectionData()
        featurecollectiondata.createCollectionsFromConnectedSegments(trajectory_path_list,
                                                                     re_initialized_trajectory_segments)

        data_path = "../../../data/"
        featurecollectiondata.writeCollection(data_path + trajectorydataloc.mapfilename + ".geojson",
                                              featurecollectiondata.all_collection)
        featurecollectiondata.writeCollection(data_path + trajectorydataloc.mapfilename + ".json",
                                              featurecollectiondata.all_collection)

        self.trajectoriesstore[trajectorydataloc.trajectorystart] = re_initialized_trajectory_segments
