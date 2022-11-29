import segment
import shapely.wkt

import Node as nd

class connectedsegments:
    def __init__(self):
        self.segments = list()
        self.postprocessed_segments = dict()

    def get_connected_segments(self, target_search_network, networkIdList):
        dist = 0
        for networkid in networkIdList:
            gdf = target_search_network[target_search_network['id'].isin([networkid])]

            for road in gdf.itertuples():
                dist = dist + road.length
                geom_str = str(road.geometry)
                geometry = shapely.wkt.loads(geom_str)
                geom = geometry.coords

                seg = segment.segment()
                startpoint = geom[0]
                endpoint = geom[1]
                seg.start = [startpoint[0], startpoint[1]]
                seg.end = [endpoint[0], endpoint[1]]
                seg.cumDist = dist
                seg.maxspeed = road.maxspeed
                seg.id = road.id

                speed_m_per_secs = (1000.0 * road.maxspeed) / 3600
                seg.travel_time = (dist / speed_m_per_secs)

                self.segments.append(seg)

    def __getallincoming(self, initializedsegments, currentsegmentid):
        initializedsegment: segment.segment = initializedsegments[ currentsegmentid]
        incomingsegments: list = initializedsegment.predecessors
        allincoming = list()
        while incomingsegments is not None:
            for currentsegmentidloc in incomingsegments:
                allincoming.append(currentsegmentidloc)
                currentsegmentid = currentsegmentidloc
            initializedsegment: segment.segment = initializedsegments[currentsegmentid]
            incomingsegments: list = initializedsegment.predecessors
        return allincoming.reverse()

    def get_last_node(self, nodeslist: list) -> nd.Node:
        nodeloc: nd.Node = None
        for node in nodeslist:
            nodeloc = node
        return nodeloc

    def __reordernodes(self, initializedsegments: dict, visitedset: list) -> None:
        node_cnt = 1
        for roadid in visitedset:
            initializedsegment: segment.segment = initializedsegments[roadid]
            nodeslist: list = initializedsegment.nodes.nodeslist
            reorderednodes = list()
            for node in nodeslist:
                node.setNodeId(node_cnt)
                reorderednodes.append(node)
                node_cnt = node_cnt + 1
            initializedsegment.nodes.nodeslist = reorderednodes
            initializedsegments[roadid] = initializedsegment
        return initializedsegments

    def __reordernodesext(self, datastorforvisitedsets: dict, preprocessedsegments: dict) -> dict:
        for key in datastorforvisitedsets.keys():

            visitedset: list = datastorforvisitedsets[key]
            node_cnt = 1
            for roadid in visitedset:
                preprocessedsegment: segment.segment = preprocessedsegments[roadid]
                nodeslist: list = preprocessedsegment.nodes.nodeslist
                incomingsegments: list = preprocessedsegment.predecessors
                if incomingsegments is not None and len(incomingsegments) >= 1:
                    incomingsegment = incomingsegments[0]
                    print("reseting incoming-: ", roadid, ", incoming", incomingsegment)
                    preprocessedincomingsegment: segment.segment = preprocessedsegments[incomingsegment]
                    nodeslistloc: list = preprocessedincomingsegment.nodes.nodeslist
                    reorderednodesloc = list()
                    for node in nodeslistloc:
                        node.setNodeId(node_cnt)
                        reorderednodesloc.append(node)
                        node_cnt = node_cnt + 1
                    preprocessedincomingsegment.nodes.nodeslist = reorderednodesloc
                    preprocessedsegments[incomingsegment] = preprocessedincomingsegment
                    preprocessedsegment.predecessors = [incomingsegment]
                    preprocessedsegments[roadid] = preprocessedsegment

                reorderednodes = list()
                for node in nodeslist:
                    node.setNodeId(node_cnt)
                    reorderednodes.append(node)
                    node_cnt = node_cnt + 1
                preprocessedsegment.nodes.nodeslist = reorderednodes
                preprocessedsegments[roadid] = preprocessedsegment
        return preprocessedsegments

    def build_connected_segments(self, datastorforvisitedsets: dict, preprocessed_segments: dict):

        ##re_preprocessedsegments = self.__reordernodesext(datastorforvisitedsets, preprocessed_segments)
        for key in datastorforvisitedsets.keys():
            visitedset: list = datastorforvisitedsets[key]

            for roadid in visitedset:
                preprocessedsegment: segment.segment = preprocessed_segments[roadid]
                nodeslist: list = preprocessedsegment.nodes.nodeslist
                incomingids = preprocessedsegment.predecessors
                if len(incomingids) >= 1:
                    incomingid = incomingids[0]
                    incomingseg: segment.segment = preprocessed_segments[incomingid]
                    print("build_connected_segments-: ", roadid, ", incoming", incomingid)
                    lastnode:nd.Node = self.get_last_node(incomingseg.nodes.nodeslist)

                    preprocessedsegment.nodeslist.append(lastnode)
                    preprocessedsegment.start = lastnode.nodeId
                    endnode:nd.Node = None
                    node_cnt = lastnode.nodeId
                    for node in nodeslist:
                        node.setNodeId(node_cnt)
                        node_cnt = node_cnt + 1
                        endnode = node
                    preprocessedsegment.end = endnode.nodeId
                    preprocessedsegment.nodeslist.append(endnode)
                    preprocessed_segments[roadid] = preprocessedsegment
                    preprocessedsegment.printsegment()
                else:
                    firstnode: nd.Node = preprocessedsegment.nodes.nodeslist[0]

                    lastnode: nd.Node = self.get_last_node(preprocessedsegment.nodes.nodeslist)

                    preprocessedsegment.nodeslist.append(firstnode)
                    preprocessedsegment.nodeslist.append(lastnode)
                    preprocessedsegment.start = firstnode.nodeId
                    preprocessedsegment.end = lastnode.nodeId
                    preprocessed_segments[roadid] = preprocessedsegment
                    preprocessedsegment.printsegment()
        return  preprocessed_segments







