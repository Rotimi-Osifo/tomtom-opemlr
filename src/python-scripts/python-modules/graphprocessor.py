from geojson import LineString
import shapely.wkt as shwkt

import GeometryData as gData
import Node
import Nodes
import CummulativeDistanceAndTime
import graphfunctions as graphfxns

import segment

class graphprocessor:

    def __init__(self):
        self.preprocessed_segments = dict()

    def preprocesse(self, graphnetwork, startid:int, endid: int, lanedirection: int) -> dict:  # uses graph functionality in the graph network
        geometrydata = gData.GeometryData()
        preprocessed_segments = dict()

        coord_cnt = 0

        graphfuncs = graphfxns.graphfunctions()

        path:list = graphfuncs.getpath(graphnetwork, startid, endid) # path from start segment to the end segment
        path.insert(0, startid)
        cumdistance = 0  # cummulative distance from start of trajectory to the end node of this segment.
        for roadid in path:
            seg = segment.segment()
            gdf = graphnetwork[graphnetwork['id'].isin([roadid])]  # data for a single line segment as a gdf
            highway:str = graphfuncs.gethighway(gdf)
            coords_list = list()
            length = 0
            nodes: Nodes = Nodes.Nodes()

            # print("current id-: ", road.id, ", cnt-: ", cnt)
            for roadloc in gdf.itertuples():
                geom_str = str(roadloc.geometry)
                geometry = shwkt.loads(geom_str)
                geom = geometry.coords
                length = length + (roadloc.length)
                cumdistance = cumdistance + (roadloc.length)

                for point in geom:
                    coords_list.append((float(point[0]), float(point[1])))

            reduced_coords_list = list()
            prev = [0.0, 0, 0]
            print("start of logging: roadid-: ", roadid, ", coord_cnt-: ", coord_cnt)
            for coord in coords_list:
                if not geometrydata.pointsAreEqual(coord, prev):
                    coord_cnt = coord_cnt + 1
                    node = Node.Node()
                    node.setCoordinate(coord)
                    node.setNodeId(coord_cnt)
                    node.setRoadId(int(roadid))
                    node.setnodename(int(roadid))
                    nodes.addToNodesList(node)
                    reduced_coords_list.append(coord)
                     # print("current id-: ", road.id, ", cnt-: ", cnt, ", cord_cnt-: ", coord_cnt, ", len(coords_list) -:", len(coords_list))
                    prev = coord
            print("end of logging: roadid-: ", roadid, ", coord_cnt-: ", coord_cnt)

            linegeom = LineString(reduced_coords_list)
            seg.geometry = linegeom
            seg.lastv = graphfuncs.get_last_v(gdf)
            seg.firstu = graphfuncs.get_first_u(gdf)
            # outgoing segments from the current
            seg.successors = graphfuncs.successors_from_path(path, roadid, endid) #.getpath(graphnetwork, roadid, endid) #(graphnetwork, seg.lastv)
            print("Current roadid -: ", roadid)
            print("successors -: ", seg.successors)
            # incoming segments to the current
            seg.predecessors = graphfuncs.predecessors_from_path(path, roadid, startid) #.getreversepath(graphnetwork, roadid, startid, path)
            print("predecessors -: ", seg.predecessors)
            seg.length = length
            seg.cumDist = cumdistance
            seg.id = roadid
            seg.nodes = nodes
            seg.setFow(highway)
            seg.setFrc(highway)
            seg.direction = lanedirection
            seg.maxspeed = CummulativeDistanceAndTime.road_class_to_kmph(highway)
            # print("incoming line id-: ", seg.incoming, ", current line id-: ", seg.id, ", out going line id-:  ", seg.outgoing, ", length-: ", seg.length)
            preprocessed_segments[roadid] = seg
        return preprocessed_segments


    def preprocess_test(self, graphnetwork, startid:int, endid:int): # uses graph functionality in the graph network
        graphfuncs = graphfxns.graphfunctions()
        successorslist:list = list()
        predecessorslist:list = list()

        successors = graphfuncs.forwardtraversalext(graphnetwork, startid, endid, successorslist)

        predecessors = graphfuncs.tracebacktrajectoryext(graphnetwork, endid, startid, predecessorslist)
        #print(len(predecessors))

        return(predecessors, successors)