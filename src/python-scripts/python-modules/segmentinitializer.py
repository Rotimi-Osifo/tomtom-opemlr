from geojson import LineString
import shapely.wkt as shwkt

import GeometryData as gData
import Node
import Nodes
import CummulativeDistanceAndTime

import segment


class segmentinitializer:

    def __init__(self):
        self.initialized_segments = dict()

    def __get_last_v(self, gdf): # uses graph functionality in the graph network
        last_v = None
        for seg in gdf.itertuples():
            last_v = seg.v
        return last_v

    def __get_first_u(self, gdf): # uses graph functionality in the graph network
        for seg in gdf.itertuples():
            return seg.u

    def __getincomingline(self, graphnetwork, firstu): # uses graph functionality in the graph network
        for road in graphnetwork.itertuples():
            if road.v == firstu: # firstu of the current segment
                return road.id
        return None

    def __getoutgoingline(self, graphnetwork, lastv): # uses graph functionality in the graph network
        for road in graphnetwork.itertuples():
            if road.u == lastv: # lastv of the current segment
                return road.id
        return None

    def initialize_segments(self, graphnetwork): # uses graph functionality in the graph network
        geometrydata = gData.GeometryData()
        cnt = 0
        coord_cnt = 0
        prev_roadid = -1
        for road in graphnetwork.itertuples():
            if road.id != prev_roadid:
                seg = segment.segment()
                gdf = graphnetwork[graphnetwork['id'].isin([road.id])]  # data for a single line segment as a gdf
                coords_list = list()
                length = 0
                nodes:Nodes = Nodes.Nodes()
                cnt = cnt + 1
                print("current id-: ", road.id, ", cnt-: ", cnt)
                for roadloc in gdf.itertuples():
                    geom_str = str(roadloc.geometry)
                    geometry = shwkt.loads(geom_str)
                    geom = geometry.coords
                    length = length + (roadloc.length)

                    for point in geom:
                        coords_list.append((float(point[0]), float(point[1])))

                reduced_coords_list = list()
                prev = [0.0, 0, 0]
                for coord in coords_list:
                    if not geometrydata.pointsAreEqual(coord, prev):
                        coord_cnt = coord_cnt + 1
                        node = Node.Node()
                        node.setCoordinate(coord)
                        node.setNodeId(coord_cnt)
                        node.setRoadId(int(road.id))
                        node.setnodename(int(road.id))
                        nodes.addToNodesList(node)
                        reduced_coords_list.append(coord)
                        print("current id-: ", road.id, ", cnt-: ", cnt, ", cord_cnt-: ", coord_cnt, ", len(coords_list) -:", len(coords_list))
                    prev = coord

                linegeom = LineString(reduced_coords_list)
                seg.geometry= linegeom
                seg.lastv = self.__get_last_v(gdf)
                seg.firstu = self.__get_first_u(gdf)
                seg.successors = self.__getoutgoingline(graphnetwork, seg.lastv) # incoming segment to the current
                seg.predecessors = self.__getincomingline(graphnetwork, seg.firstu) # out going segment from the current
                seg.length = length
                seg.id = road.id
                seg.nodes = nodes
                seg.setFow(road.highway)
                seg.setFrc(road.highway)
                seg.maxspeed = CummulativeDistanceAndTime.road_class_to_kmph(road.highway)
                print("incoming line id-: ", seg.predecessors, ", current line id-: ", seg.id, ", out going line id-:  ", seg.successors, ", length-: ", seg.length)
                self.initialized_segments[road.id] = seg
                prev_roadid = road.id