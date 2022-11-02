import Nodes
import Node as nd
import GeometryData as gData
import shapely.wkt as shwkt
import neighbour_search as nb_s

class NodesCreator:
    def __init__(self):
        self.nodes: Nodes = None

    def createnodesfromgraph(self, graphroadnetwork, networkIdList):
        self.nodes = Nodes.Nodes()

        coord_cnt = 0
        cnt = 0

        geometrydata = gData.GeometryData()

        prevnode = None
        for networkid in networkIdList:
            gdf = graphroadnetwork[graphroadnetwork['id'].isin([networkid])]

            segmentnodes = list()
            for road in gdf.itertuples():
                geom_str = str(road.geometry)
                geometry = shwkt.loads(geom_str)
                geom = geometry.coords

                startnode = nd.Node()
                startpoint = geom[0]

                if cnt < 2:
                    cnt = cnt + 1
                    coord_cnt = coord_cnt + 1
                    print(cnt, " ", coord_cnt, " ", road.id)
                    startnode.setCoordinate([startpoint[0], startpoint[1]])
                    startnode.setNodeId(coord_cnt)
                    startnode.setRoadId(int(road.id))
                    startnode.setnodename(int(road.id))
                    segmentnodes.append(startnode)

                    endnode = nd.Node()
                    endpoint = geom[1]
                    cnt = cnt + 1
                    coord_cnt = coord_cnt + 1
                    print(cnt, " ", coord_cnt, " ", road.id)
                    endnode.setCoordinate([endpoint[0], endpoint[1]])
                    endnode.setNodeId(coord_cnt)
                    endnode.setRoadId(int(road.id))
                    endnode.setnodename(int(road.id))
                    segmentnodes.append(endnode)

                else:

                    node = nd.Node()
                    point = geom[1]
                    cnt = cnt + 1
                    print(cnt, " ", coord_cnt, " ", road.id)
                    node.setCoordinate([point[0], point[1]])
                    node.setRoadId(int(road.id))
                    node.setnodename(int(road.id))
                    if not self.nodes.hassamecoords(node, prevnode):
                        coord_cnt = coord_cnt + 1
                        node.setNodeId(coord_cnt)
                        segmentnodes.append(node)


                    prevnode = node
            print(networkid, " ", len(segmentnodes))
            self.nodes.addToNodes(segmentnodes, networkid)
            #self.nodes.printnodes()
        return self.nodes







