import Node as nd
import Line as ln
import Lines as lns
import shapely.wkt as shwkt
import GeometryData as gData
import Nodes
from geojson import LineString

import line_data_initializer


class LinesCreator:
    def __init__(self):
        self.lines = None
        self.nodes = None

    def __get_last_v(self, gdf):
        last_v = None
        for seg in gdf.itertuples():
            last_v = seg.v
        return last_v

    def __get_first_u(self, gdf):
        for seg in gdf.itertuples():
            return seg.u

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

        self.nodes = Nodes.Nodes()

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
                    print("Not the same same -: ", road.id, " ", coord_cnt)
                    startnode.setCoordinate([startpoint[0], startpoint[1]])
                    startnode.setNodeId(coord_cnt)
                    startnode.setRoadId(int(road.id))
                    startnode.setnodename(int(road.id))

                    line.setStartNodeId(coord_cnt)
                    line.addNode(startnode, coord_cnt)
                    line.setGeometry(geom)
                    coord_cnt = coord_cnt + 1

                else:
                    startpoint = prev
                    startnode.setCoordinate([startpoint[0], startpoint[1]])
                    startnode.setNodeId(prev_node.nodeId)
                    startnode.setRoadId(prev_node.roadId)
                    startnode.setnodename(prev_node.name)
                    line.setStartNodeId(prev_node.nodeId)
                    line.addNode(startnode, prev_node.nodeId)
                    line.setGeometry(geom)
                    coord_cnt = coord_cnt + 1

                self.nodes.addToNodes(startnode)

                line.setHighway(road.highway)
                line.setRoadId(int(road.id))
                line.setLength(int(road.length))
                line.setFrc(road.highway)
                line.setFow(road.highway)
                line.setincominglineid(incominglineid)


                endnode = nd.Node()
                endpoint = geom[1]
                endnode.setCoordinate([endpoint[0], endpoint[1]])
                endnode.setNodeId(coord_cnt)
                endnode.setRoadId(int(road.id))
                endnode.setnodename(int(road.id))
                prev = endpoint
                prev_node = endnode
                self.nodes.addToNodes(endnode)

                line.setEndNodeId(coord_cnt)
                line.addNode( endnode, coord_cnt)
                line.setDirection(int(1))

                segmentlines.append(line)
                coord_cnt = coord_cnt + 1

                self.nodes.printnodes()

            lines.addLine(networkid, segmentlines)
            incominglineid = networkid
        self.lines = lines
        return lines

    def __createSegmentWithNodes(self, currentsegmentnodes: list, roadsegment_gdf, prevsegmentnodes: list,  direction):

        length = 0

        geometrydata = gData.GeometryData()

        coords_list = list()
        for road in roadsegment_gdf.itertuples():
            length = length + road.length
            geom_str = str(road.geometry)
            geometry = shwkt.loads(geom_str)
            geom = geometry.coords
            prev = [0.0, 0,0]

            for point in geom:
                coords_list.append((point[0], point[1]))

        reduced_coords_list = list()
        for coord in coords_list:
            if not geometrydata.pointsAreEqual(coord, prev):
                reduced_coords_list.append(coord)
            prev = coord

        linegeom = LineString(reduced_coords_list)
        print(linegeom)

        row_data = roadsegment_gdf.iloc[0]
        line = ln.Line()
        line.setHighway(row_data.highway)
        line.setRoadId(int(row_data.id))
        line.setLength(length)
        line.setFrc(row_data.highway)
        line.setFow(row_data.highway)
        line.setDirection(int(direction))
        line.setFirstU(int(self.__get_first_u(roadsegment_gdf)))
        line.setLastV(int(self.__get_last_v(roadsegment_gdf)))


        line.setGeometry(linegeom)
        if prevsegmentnodes is not None:
            pos = len(prevsegmentnodes) - 1
            lastpos = len(currentsegmentnodes) - 1
            if pos >= 0 and lastpos >= 0:
                firstnode: nd.Node = prevsegmentnodes[pos]
                firstnode.setnodename(int(row_data.id))
                firstnode.setRoadId(int(row_data.id))
                line.setStartNodeId(firstnode.nodeId)
                line.addNode(firstnode, firstnode.nodeId)
                line.setincominglineid(int(firstnode.roadId)) #the incoming roadid to this line

                lastnode = currentsegmentnodes[lastpos]
                line.setEndNodeId(lastnode.nodeId)
                line.addNode(lastnode, lastnode.nodeId)
            else:
                return None
        else:
            firstnode = currentsegmentnodes[0]
            line.setStartNodeId(firstnode.nodeId)
            line.addNode(firstnode, firstnode.nodeId)

            lastpos = len(currentsegmentnodes) - 1
            lastnode = currentsegmentnodes[lastpos]
            line.setEndNodeId(lastnode.nodeId)
            line.addNode(lastnode, lastnode.nodeId)

        return line


    def createConnectedRoadSegmentsFromGraph(self, graphroadnetwork, nodes: Nodes.Nodes,  direction): # graphroadnetwork  must have graphs: u = from node and v = end node
        self.lines = lns.Lines()
        prevsegmentnodes = None
        for key in nodes.keys():
            segmentnodes = nodes[key]
            gdf = graphroadnetwork[graphroadnetwork['id'].isin([key])]
            line = self.__createSegmentWithNodes(segmentnodes, gdf, prevsegmentnodes,  direction)
            if line is not None:
                self.lines.addLine(key, line)

            prevsegmentnodes = segmentnodes
        return self.lines
    
    def __getconnectedline(self, lines: dict, v):
        for key in lines.keys():
            line = lines[key]
            if line.firstu is not None:
                if line.firstu == v:
                    return line
        return None
    
    
    def __buildForwardAndBackwardConnectionsFromGraph(self, graphroadnetwork):
        initializedlines:dict = line_data_initializer.initializelines(graphroadnetwork) 
        for key in initializedlines.keys():
            this_line = initializedlines[key]
            nextline = self.__getconnectedline(initializedlines, this_line.lastv) #nextline forward
            if nextline is not None:
                this_line.setoutgoinglineid(nextline.roadId)
                if nextline.ncominglineid is None:
                    nextline.setincominglineid(key)
                    initializedlines.pop(nextline.roadId)
                    initializedlines[nextline.roadId] = nextline
            
            initializedlines.pop(key)
            initializedlines[key] = this_line
            
        return initializedlines
    
    def __getlastnodefromnodesdict(self, nodes):
        n = None
        for key in nodes:
            n = nodes[key]
        return n
    
    def __getfirstnodefromnodesdict(self, nodes):
        for key in nodes:
            return nodes[key]
    
    
    
    def __buildSegmentWithNodes(self, lines: dict,  nodes: dict, direction, key):

        line:ln.Line = lines[key] 
        incoming = line.incominglineid
        currentroadsegmentnodes:dict = nodes[key]
        line.setDirection(int(direction))
        

        if incoming is not None:
            prevsegmentnodes = nodes[incoming]
            prevsegmentnode = self.__getlastnodefromnodesdict(prevsegmentnodes)
            
            if prevsegmentnode is not None:
                firstnode: nd.Node = prevsegmentnode
                firstnode.setnodename(int(key))
                firstnode.setRoadId(int(key))
                line.setStartNodeId(firstnode.nodeId)
                line.addNode(firstnode, firstnode.nodeId)

                lastnode = self.__getlastnodefromnodesdict(currentroadsegmentnodes)
                line.setEndNodeId(lastnode.nodeId)
                line.addNode(lastnode, lastnode.nodeId)
            else:
                return None
        else:
            firstnode = self.__getfirstnodefromnodesdict(currentroadsegmentnodes)
            line.setStartNodeId(firstnode.nodeId)
            line.addNode(firstnode, firstnode.nodeId)

            lastnode = self.__getlastnodefromnodesdict(currentroadsegmentnodes)
            line.setEndNodeId(lastnode.nodeId)
            line.addNode(lastnode, lastnode.nodeId)

        return line
    
    def  buildConnectedRoadSegmentsFromGraph(self, graphroadnetwork, nodes: Nodes.Nodes,  direction):
        
        initializedlines = self.__buildForwardAndBackwardConnectionsFromGraph(graphroadnetwork)
        for key in  initializedlines.keys():
            
            line = self.__buildSegmentWithNodes(initializedlines,  nodes, direction, key)

            if line is not None:
                self.lines.addLine(key, line)

        return self.lines
    

        
        
        


