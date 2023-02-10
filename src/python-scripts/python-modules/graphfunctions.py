import geopandas as geopandas

import segment
import utilities

import Node


class graphfunctions:
    def __init__(selfself):
        pass

    def get_point_from_nodes(self, nodes, nodeid: int):
        gdf_node = nodes[nodes['id'].isin([nodeid])]
        for node in gdf_node.itertuples():
            print(node.geometry)
            return node.geometry

    def gethighway(self, gdf: geopandas) -> str:
        for seg in gdf.itertuples():
            return seg.highway

    def get_last_v(self, gdf: geopandas) -> int: # uses graph functionality in the graph network
        last_v = None
        for seg in gdf.itertuples():
            last_v = seg.v
        return last_v

    def get_first_u(self, gdf: geopandas) -> int: # uses graph functionality in the graph network
        for seg in gdf.itertuples():
            return seg.u

    def getpredecessors(self, graphnetwork: geopandas, firstu, path: list) -> list: # uses graph functionality in the graph network
        idslist = list()
        for road in graphnetwork.itertuples():
            if road.v == firstu: # firstu of the current segment
                if path.count(road.id) >= 1:
                    idslist.append(road.id)
        return idslist

    def getreversepath(self, graphnetwork: geopandas, currentsegmentid: int, startid: int, path:list) -> list:  # uses graph functionality in the graph network
        tracebacklist = list()
        return self.tracebacktrajectoryext(graphnetwork, currentsegmentid,  startid, path, tracebacklist)

    def getsuccessors(self, graphnetwork: geopandas, lastv) -> list: # uses graph functionality in the graph network
        idslist = list()
        for road in graphnetwork.itertuples():
            if road.u == lastv: # lastv of the current segment
                idslist.append(road.id)
        return idslist

    def comparelengths(self, maingraphnetwork: geopandas, firstid: int, secondid: int):
        gdffirst = maingraphnetwork[maingraphnetwork['id'].isin([firstid])]
        gdfsecond = maingraphnetwork[maingraphnetwork['id'].isin([secondid])]

        lengthfirst:float = 0.0
        for road in gdffirst.itertuples():
            lengthfirst = lengthfirst + (road.length)

        lengthsecond: float = 0.0
        for road2 in gdfsecond.itertuples():
            lengthsecond = lengthsecond + (road2.length)

        print("first length-:  ", lengthfirst, " secondlength-: ", lengthsecond, "first id-:  ", firstid, " secondid-: ", secondid)
        if lengthsecond > lengthfirst:
            return secondid
        return firstid

    def getpath(self, graphnetwork: geopandas, currentsegmentid: int, endid: int) -> list: # uses graph functionality in the graph network
        forwartraversllist = list()
        return self.forwardtraversalext(graphnetwork, currentsegmentid, endid, forwartraversllist)

    def successors_from_path(self, path: list, roadid: int, endid: int):

        if roadid == endid:
            return None # No more successor

        idx: int = utilities.get_index_of_item_from_list(path, roadid)

        successors: list = list()

        idx = idx + 1 # step forward # over the index for the curret road id
        while idx < len(path):
            successors.append(path[idx])
            idx = idx + 1

        return successors

    def predecessors_from_path(self, path: list, roadid: int, startid:int):

        if startid == roadid:
            return None # no predecessors

        predecessors: list = list()
        idx: int = utilities.get_index_of_item_from_list(path, roadid)
        idx = idx - 1  # step backwards over the index for the curret road id
        while idx >= 0:
            predecessors.append(path[idx])
            idx = idx - 1

        return predecessors

    def tracebacktrajectory(self, preproceesedsegments: dict, currentsegmentid: int, startid: int, tracebacklist: list):

        preprocessedsegment: segment.segment = preproceesedsegments[currentsegmentid]
        predecessors: list = preprocessedsegment.predecessors
        if predecessors is None:
           return tracebacklist
        else:
            if len(predecessors) == 1:
                tracebacklist.append(predecessors[0])
                if tracebacklist.count(startid) >= 1:
                    return tracebacklist
                else:
                    return self.tracebacktrajectory(preproceesedsegments, predecessors[0], startid, tracebacklist)
            elif len(predecessors) == 2:
                predecessorfirst = predecessors[0]
                tracebacklist.append(predecessorfirst)

                if tracebacklist.count(startid) >= 1:
                    return tracebacklist
                else:
                    return self.tracebacktrajectory(preproceesedsegments, predecessorfirst, startid, tracebacklist)

                predecessorsecond = predecessors[1]
                tracebacklist.append(predecessorsecond)
                if tracebacklist.count(startid) >= 1:
                    return tracebacklist
                else:
                    return self.tracebacktrajectory(preproceesedsegments, predecessorsecond, startid, tracebacklist)

    def tracebacktrajectoryext(self, maingraphnetwork, currentsegmentid: int, startid: int, path: list, tracebacklist: list):
        gdf = maingraphnetwork[maingraphnetwork['id'].isin([currentsegmentid])]
        firstu: int = self.get_first_u(gdf)

        predecessors: list = self.getpredecessors(maingraphnetwork, firstu, path)

        if predecessors is None:
            if currentsegmentid == startid:
                tracebacklist.append(currentsegmentid)
            return tracebacklist
        else:
            if len(predecessors) == 1:
                tracebacklist.append(predecessors[0])
                if tracebacklist.count(startid) >= 1:
                    return tracebacklist
                else:
                    return self.tracebacktrajectoryext(maingraphnetwork, predecessors[0], startid, path, tracebacklist)
            elif len(predecessors) == 2:
                predecessorfirst = predecessors[0]
                tracebacklist.append(predecessorfirst)
                if tracebacklist.count(startid) >= 1:
                    print("predecessorfirst - inside return -:", predecessorfirst)
                    return tracebacklist
                else:
                    print("predecessorfirst - inside recursion -:", predecessorfirst)
                    return self.tracebacktrajectoryext(maingraphnetwork, predecessorfirst, startid, path, tracebacklist)

                predecessorsecond = predecessors[1]
                tracebacklist.append(predecessorsecond)
                if tracebacklist.count(startid) >= 1:
                    print("predecessorsecond - inside return -:", predecessorsecond)
                    return tracebacklist
                else:
                    print("predecessorsecond - inside recursion -:", predecessorsecond)
                    return self.tracebacktrajectoryext(maingraphnetwork, predecessorsecond, startid, path, tracebacklist)
        return tracebacklist

    def forwardtraversalext(self, maingraphnetwork, currentsegmentid: int, endid: int, forwardtraversallist: list):
        gdf = maingraphnetwork[maingraphnetwork['id'].isin([currentsegmentid])]
        lastv :int = self.get_last_v(gdf)

        successors: list = self.getsuccessors(maingraphnetwork, lastv)

        #if currentsegmentid == 1060974763:

        #print("current id -: ", currentsegmentid, "endid -: ", endid, "len successors -: ", len( successors))
        if successors is None:
            if  currentsegmentid == endid:
                forwardtraversallist.append(currentsegmentid)
            return forwardtraversallist
        else:
            if len(successors) == 1:
                forwardtraversallist.append(successors[0])
                if forwardtraversallist.count(endid) >= 1:
                    return forwardtraversallist
                else:
                    return self.forwardtraversalext(maingraphnetwork, successors[0], endid, forwardtraversallist)
            elif len(successors) == 2:
                succssorfirst = successors[0]
                forwardtraversallist.append(succssorfirst)

                if forwardtraversallist.count(endid) >= 1:
                    return forwardtraversallist
                else:
                    return self.forwardtraversalext(maingraphnetwork, succssorfirst , endid, forwardtraversallist)

                sucessorsecond = successors[1]
                forwardtraversallist.append(sucessorsecond)
                if forwardtraversallist.count(endid) >= 1:
                    return forwartraversllist
                else:
                    return self.forwardtraversalext(maingraphnetwork, sucessorsecond, endid, forwardtraversallist)

        return forwardtraversallist

    def forwardtraversal(self, preproceesedsegments: dict, currentsegmentid: int, endid: int, forwartraversllist: list):

        preprocessedsegment: segment.segment = preproceesedsegments[currentsegmentid]
        successors: list = preprocessedsegment.successors
        if successors is None:
            return forwartraversllist
        else:
            if len(successors) == 1:
                forwartraversllist.append(successors[0])
                if forwartraversllist.count(endid) >= 1:
                    return forwartraversllist
                else:
                    return self.tracebacktrajectory(preproceesedsegments, successors[0], endid, forwartraversllist)
            elif len(successors) == 2:
                succssorfirst = successors[0]
                forwartraversllist.append(succssorfirst)

                if forwartraversllist.count(endid) >= 1:
                    return forwartraversllist
                else:
                    return self.tracebacktrajectory(preproceesedsegments, succssorfirst, endid, forwartraversllist)

                sucessorsecond = successors[1]
                forwartraversllist.append(sucessorsecond)
                if forwartraversllist.count(endid) >= 1:
                    return forwartraversllist
                else:
                    return self.tracebacktrajectory(preproceesedsegments, predecessorsecond, endid, forwartraversllist)

    def tracebackincoming(self, initializedsegments: dict, currentsegmentid: int, tracebacklist: list):

        initializedsegment: segment.segment = initializedsegments[currentsegmentid]
        incomingsegments: list = initializedsegment.predecessors
        if incomingsegments is not None and len(incomingsegments) >= 1:
            for incomingsegment in incomingsegments:
                initializedsegmentloc: segment.segment = initializedsegments[incomingsegment]
                incomingsegmentsloc: list = initializedsegmentloc.predecessors
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
                incomingsegments: list = initializedsegment.predecessors
                if incomingsegments is not None and len(incomingsegments) >= 1:
                    tracebacklist = list()
                    self.tracebackincoming(initializedsegments, roadid, tracebacklist)
                    if tracebacklist is not None:
                        tracebacklistdict[roadid] = tracebacklist
            except:
                print("the key-: ", roadid, " is not in the dictionary!")
        return tracebacklistdict

    def printsegments(self, segments_: dict) -> None:
        for key in segments_.keys():
            segment_ = segments_[key]
            nodes:dict = segment_.nodes.nodes
            for k in nodes.keys():
                nodeslist:list = nodes[k]
                for node in nodeslist:
                    n:Node.Node = node
                    n.printnode()