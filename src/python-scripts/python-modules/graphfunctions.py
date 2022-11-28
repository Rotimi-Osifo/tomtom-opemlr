import geopandas as geopandas
import segment
import Node
import graphfunctions as graphfxns

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

    def getpredecessors(self, graphnetwork: geopandas, firstu) -> list: # uses graph functionality in the graph network
        idslist = list()
        for road in graphnetwork.itertuples():
            if road.v == firstu: # firstu of the current segment
                idslist.append(road.id)
        return idslist

    def getreversepath(self, graphnetwork: geopandas, currentsegmentid: int, startid: int) -> list:  # uses graph functionality in the graph network
        tracebacklist = list()
        return self.tracebacktrajectoryext(graphnetwork, currentsegmentid,  startid, tracebacklist)

    def getsuccessors(self, graphnetwork: geopandas, lastv) -> list: # uses graph functionality in the graph network
        idslist = list()
        for road in graphnetwork.itertuples():
            if road.u == lastv: # lastv of the current segment
                idslist.append(road.id)
        return idslist

    def getpath(self, graphnetwork: geopandas, currentsegmentid: int, endid: int) -> list: # uses graph functionality in the graph network
        forwartraversllist = list()
        return self.forwardtraversalext(graphnetwork, currentsegmentid, endid, forwartraversllist)

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

    def tracebacktrajectoryext(self, maingraphnetwork, currentsegmentid: int, startid: int, tracebacklist: list):
        gdf = maingraphnetwork[maingraphnetwork['id'].isin([currentsegmentid])]
        firstu: int = self.get_first_u(gdf)

        predecessors: list = self.getpredecessors(maingraphnetwork, firstu)

        if predecessors is None:
            return tracebacklist
        else:
            if len(predecessors) == 1:
                if tracebacklist.count(startid) >= 1:
                    return tracebacklist
                else:
                    tracebacklist.append(predecessors[0])
                    return self.tracebacktrajectoryext(maingraphnetwork, predecessors[0], startid, tracebacklist)
            elif len(predecessors) == 2:
                predecessorfirst = predecessors[0]
                if tracebacklist.count(startid) >= 1:
                    return tracebacklist
                else:
                    tracebacklist.append(predecessorfirst)
                    return self.tracebacktrajectoryext(maingraphnetwork, predecessorfirst, startid, tracebacklist)

                predecessorsecond = predecessors[1]
                if tracebacklist.count(startid) >= 1:
                    return tracebacklist
                else:
                    tracebacklist.append(predecessorsecond)
                    return self.tracebacktrajectoryext(maingraphnetwork, predecessorsecond, startid, tracebacklist)
        return tracebacklist

    def forwardtraversalext(self, maingraphnetwork, currentsegmentid: int, endid: int, forwartraversllist: list):
        gdf = maingraphnetwork[maingraphnetwork['id'].isin([currentsegmentid])]
        lastv :int = self.get_last_v(gdf)

        successors: list = self.getsuccessors(maingraphnetwork, lastv)
        if successors is None:
            return forwartraversllist
        else:
            if len(successors) == 1:
                forwartraversllist.append(successors[0])
                if forwartraversllist.count(endid) >= 1:
                    return forwartraversllist
                else:
                    return self.forwardtraversalext(maingraphnetwork, successors[0], endid, forwartraversllist)
            elif len(successors) == 2:
                succssorfirst = successors[0]
                forwartraversllist.append(succssorfirst)

                if forwartraversllist.count(endid) >= 1:
                    return forwartraversllist
                else:
                    return self.forwardtraversalext(maingraphnetwork, succssorfirst, endid, forwartraversllist)

                sucessorsecond = successors[1]
                forwartraversllist.append(sucessorsecond)
                if forwartraversllist.count(endid) >= 1:
                    return forwartraversllist
                else:
                    return self.forwardtraversalext(maingraphnetwork, sucessorsecond, endid, forwartraversllist)
        return forwartraversllist

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