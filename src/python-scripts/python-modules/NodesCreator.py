import Nodes
import Node as nd
import GeometryData as gData
import shapely.wkt as shwkt
import segment

class NodesCreator:
    def __init__(self):
        self.nodes: Nodes = None
    
    
    def __hassamecoords(self, currentnode, prevnode, geometrydata):
        if prevnode is None:
            return False
        else:
            currentcoord = currentnode.coordinate
            prevcoord = prevnode.coordinate

            return geometrydata.pointsAreEqual(currentcoord, prevcoord)
        
    def buildnodesfromgraph(self, graphroadnetwork):
        self.nodes = Nodes.Nodes()

        coord_cnt = 0
        cnt = 0

        geometrydata = gData.GeometryData()
        for segment in graphroadnetwork.itertuples():
            gdf = graphroadnetwork[graphroadnetwork['id'].isin([segment.id])] # road segment geopandas
            roadsegmentnodes = dict()
            prevnode = None
            nodecount = 0
            for road in gdf.itertuples():
                segmentnodes = list()
                geom_str = str(road.geometry)
                geometry = shwkt.loads(geom_str)
                geom = geometry.coords

                startnode = nd.Node()
                startpoint = geom[0]

                if cnt < 1:
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
                    if not self.__hassamecoords(node, prevnode,  geometrydata):
                        coord_cnt = coord_cnt + 1
                        node.setNodeId(coord_cnt)
                        segmentnodes.append(node)
                        
                    prevnode = node
                
                nodecount = nodecount + 1
                roadsegmentnodes[str(nodecount)] = segmentnodes
             
            print(segment.id, " ", len(roadsegmentnodes))
            self.nodes.addToNodes(roadsegmentnodes, segment.id)
            
        return self.nodes
    
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

                if cnt < 1:
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
                    if not self.__hassamecoords(node, prevnode,  geometrydata):
                        coord_cnt = coord_cnt + 1
                        node.setNodeId(coord_cnt)
                        segmentnodes.append(node)


                    prevnode = node
            print(networkid, " ", len(segmentnodes))
            self.nodes.addToNodes(segmentnodes, networkid)
        
        return self.nodes







