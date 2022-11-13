import segment
import segmentinitializer
class roadnetworkgraphsearch:
    def __init__(self):
        self.visitedset = list()


    def __buildconnectedsegments(self, initialized_segments, startid):
        if self.visitedset.count(startid) == 0:
            self.visitedset.append(startid)
            seg:segment.segment = initialized_segments[startid]
            if seg.outgoing is not None:
                self.__buildconnectedsegments(initialized_segments, seg.outgoing)
            else:
                return self.visitedset
        else:
            return self.visitedset

    def buildconnectedsegments(self, graphnetwork, startid):
        segment_initializer = segmentinitializer.segmentinitializer()
        segment_initializer.initialize_segments(graphnetwork)
        self.__buildconnectedsegments(segment_initializer.initialized_segments, startid)
