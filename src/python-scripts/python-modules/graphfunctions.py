import geopandas as geopandas
import segment

class graphfunctions:
    def __init__(selfself):
        pass

    def get_last_v(self, gdf: geopandas) -> int: # uses graph functionality in the graph network
        last_v = None
        for seg in gdf.itertuples():
            last_v = seg.v
        return last_v

    def get_first_u(self, gdf: geopandas) -> int: # uses graph functionality in the graph network
        for seg in gdf.itertuples():
            return seg.u

    def getincomingline(self, graphnetwork: geopandas, firstu) -> int: # uses graph functionality in the graph network
        idslist = list()
        for road in graphnetwork.itertuples():
            if road.v == firstu: # firstu of the current segment
                idslist.append(road.id)
        return idslist

    def getoutgoingline(self, graphnetwork: geopandas, lastv) -> int: # uses graph functionality in the graph network
        idslist = list()
        for road in graphnetwork.itertuples():
            if road.u == lastv: # lastv of the current segment
                idslist.append(road.id)
        return idslist

    def tracebackincoming(self, initializedsegments: dict, currentsegmentid: int, tracebacklist: list):

        initializedsegment: segment.segment = initializedsegments[currentsegmentid]
        incomingsegments: list = initializedsegment.incoming
        if incomingsegments is not None and len(incomingsegments) >= 1:
            for incomingsegment in incomingsegments:
                initializedsegmentloc: segment.segment = initializedsegments[incomingsegment]
                incomingsegmentsloc: list = initializedsegmentloc.incoming
                if incomingsegmentsloc is not None:
                    tracebacklist.append(incomingsegment)
                    self.tracebackincoming(initializedsegments, incomingsegment, tracebacklist)
                # else:
                # return tracebacklist
    def getallincomingext(self, initializedsegments: dict, visitedset: list) -> dict:
        tracebacklistdict = dict()
        for roadid in visitedset:
            try:
                initializedsegment: segment.segment = initializedsegments[roadid]
                incomingsegments: list = initializedsegment.incoming
                if incomingsegments is not None and len(incomingsegments) >= 1:
                    tracebacklist = list()
                    self.tracebackincoming(initializedsegments, roadid, tracebacklist)
                    if tracebacklist is not None:
                        tracebacklistdict[roadid] = tracebacklist
            except:
                print("the key-: ", roadid, " is not in the dictionary!")
        return tracebacklistdict