import segment
import shapely.wkt

import Node as nd

class connectedsegments:
    def __init__(self):
        self.segments = list()

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


    def build_connected_segments(self, datastorforvisitedsets: dict, initializedsegments: dict):
        for key in datastorforvisitedsets.keys():
            visitedset: list = datastorforvisitedsets[key]
            self.__reordernodes(initializedsegments, visitedset)
            for roadid in visitedset:
                initializedsegment: segment.segment = initializedsegments[roadid]
                nodeslist: list = initializedsegment.nodes.nodeslist
                incomingid = initializedsegment.incoming
                if incomingid != None:
                    incomingseg: segment.segment = initializedsegments[incomingid]
                    lastnode:nd.Node = self.get_last_node(incomingseg.nodes.nodeslist)

                    initializedsegment.nodeslist.append(lastnode)
                    initializedsegment.start = lastnode.nodeId
                    endnode:nd.Node = None
                    node_cnt = lastnode.nodeId
                    for node in nodeslist:
                        node.setNodeId(node_cnt)
                        node_cnt = node_cnt + 1
                        endnode = node
                    initializedsegment.end = endnode.nodeId
                    initializedsegment.nodeslist.append(endnode)
                    initializedsegments[roadid] = initializedsegment
                    initializedsegment.printsegment()
                else:
                    lastnode: nd.Node = self.get_last_node(initializedsegment.nodes.nodeslist)
                    firstnode:nd.Node = initializedsegment.nodes.nodeslist[0]
                    initializedsegment.nodeslist.append(firstnode)
                    initializedsegment.nodeslist.append(lastnode)
                    initializedsegment.start = firstnode.nodeId
                    initializedsegment.end = lastnode.nodeId
                    initializedsegment.printsegment()







