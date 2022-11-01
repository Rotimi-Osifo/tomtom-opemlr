import Node as nd
import Line as ln
import Lines as lns
import shapely.wkt as shwkt
import GeometryData as gData

class LinesCreator:
    def __init__(self):
        self.lines = None
    
    def createLines(self, idList, geometryData, targetNetwork):
        lines = lns.Lines()
        coord_cnt = 1
        for roadId in idList:
            gdf_loc = targetNetwork[targetNetwork['id'].isin([roadId])]
        
            line = ln.Line()
            line.setStartNodeId(coord_cnt)
            for road in gdf_loc.itertuples():
                geom = geometryData.get_line_string(road.geometry)
                coordinates = geom['coordinates']
                line.setGeometry(geom)
                line.setHighway(road.highway)
                line.setRoadId(int(road.id))
                line.setLength(int(road.length))
                line.setFrc(road.highway)
                line.setFow(road.highway)

                coordinates.sort(key = lambda p: p[0])

                for point in coordinates:

                    node = nd.Node()
                    node.setCoordinate(point)
                    node.setNodeId(coord_cnt)
                    node.setRoadId(int(road.id))
                    node.setnodename(road.id)
                    
                    line.addNode(node, road.id)

                    coord_cnt = coord_cnt + 1
                line.setEndNodeId(coord_cnt - 1)
                line.setDirection(int(1))
                lines.addLine(road.id, line)
        self.lines = lines
        return lines

    def createConnectedRoadSegments(self, graphroadnetwork, networkIdList): # graphroadnetwork  must have graphs: u = from node and v = end node
        lines = lns.Lines()
        coord_cnt = 1

        geometrydata = gData.GeometryData()

        print(networkIdList)
        incominglineid = None
        for networkid in networkIdList:
            gdf = graphroadnetwork[graphroadnetwork['id'].isin([networkid])]

            # each road segment graph has several lines between each two successive nodes in the segment
            # represents one road segment id with short lines between successive coordinates
            segmentlines = list()
            prev = [0.0, 0.0]
            prev_node = None
            for road in gdf.itertuples():

                geom_str = str(road.geometry)
                geometry = shwkt.loads(geom_str)
                geom = geometry.coords


                startnode = nd.Node()
                startpoint = geom[0]

                line = ln.Line()  # line connecting 2 successive points in a road segment


                if geometrydata.pointsAreEqual(prev, startpoint) == False:
                    print("same -: ", road.id, " ", coord_cnt)
                    startnode.setCoordinate([startpoint[0], startpoint[1]])
                    startnode.setNodeId(coord_cnt)
                    startnode.setRoadId(int(road.id))
                    startnode.setnodename(int(road.id))

                    line.setStartNodeId(coord_cnt)
                    line.addNode(startnode, coord_cnt)
                    line.setGeometry(geom)
                else:
                    startpoint = prev
                    startnode.setCoordinate([startpoint[0], startpoint[1]])
                    startnode.setNodeId(prev_node.nodeId)
                    startnode.setRoadId(prev_node.roadId)
                    startnode.setnodename(prev_node.name)
                    line.setStartNodeId(prev_node.nodeId)
                    line.addNode(startnode, prev_node.nodeId)
                    line.setGeometry(geom)

                line.setHighway(road.highway)
                line.setRoadId(int(road.id))
                line.setLength(int(road.length))
                line.setFrc(road.highway)
                line.setFow(road.highway)
                line.setincominglineid(incominglineid)

                coord_cnt = coord_cnt + 1
                endnode = nd.Node()
                endpoint = geom[1]
                endnode.setCoordinate([endpoint[0], endpoint[1]])
                endnode.setNodeId(coord_cnt)
                endnode.setRoadId(int(road.id))
                endnode.setnodename(int(road.id))
                prev = endpoint
                prev_node = endnode

                line.setEndNodeId(coord_cnt)
                line.addNode( endnode, coord_cnt)
                line.setDirection(int(1))

                segmentlines.append(line)
                coord_cnt = coord_cnt + 1

            lines.addLine(networkid, segmentlines)
            incominglineid = networkid
        self.lines = lines
        return lines

            
    
        
        
        
        
        


