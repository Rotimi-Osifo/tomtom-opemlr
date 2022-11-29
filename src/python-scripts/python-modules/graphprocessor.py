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

    def preprocess(self, graphnetwork): # uses graph functionality in the graph network
        geometrydata = gData.GeometryData()
        cnt = 0
        coord_cnt = 0
        prev_roadid = -1
        graphfuncs = graphfxns.graphfunctions()
        cumdistance = 0 # cummulative distance from start of trajectory to the end node of this segment.
        for road in graphnetwork.itertuples():
            if road.id != prev_roadid:
                seg = segment.segment()
                gdf = graphnetwork[graphnetwork['id'].isin([road.id])]  # data for a single line segment as a gdf
                coords_list = list()
                length = 0
                nodes:Nodes = Nodes.Nodes()
                cnt = cnt + 1
                #print("current id-: ", road.id, ", cnt-: ", cnt)
                for roadloc in gdf.itertuples():
                    geom_str = str(roadloc.geometry)
                    geometry = shwkt.loads(geom_str)
                    geom = geometry.coords
                    length = length + (roadloc.length)
                    cumdistance =  cumdistance + (roadloc.length)

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
                        #print("current id-: ", road.id, ", cnt-: ", cnt, ", cord_cnt-: ", coord_cnt, ", len(coords_list) -:", len(coords_list))
                    prev = coord

                linegeom = LineString(reduced_coords_list)
                seg.geometry= linegeom
                seg.lastv = graphfuncs.get_last_v(gdf)
                seg.firstu = graphfuncs.get_first_u(gdf)
                seg.successors = graphfuncs.getsuccessors(graphnetwork, seg.lastv) # outgoing segment from the current
                seg.predecessors = graphfuncs.getpredecessors(graphnetwork, seg.firstu) # incoming segment to the current
                seg.length = length
                seg.cumDist = cumdistance
                seg.id = road.id
                seg.nodes = nodes
                seg.setFow(road.highway)
                seg.setFrc(road.highway)
                seg.maxspeed = CummulativeDistanceAndTime.road_class_to_kmph(road.highway)
                #print("incoming line id-: ", seg.incoming, ", current line id-: ", seg.id, ", out going line id-:  ", seg.outgoing, ", length-: ", seg.length)
                self.preprocessed_segments[road.id] = seg
                prev_roadid = road.id

    def preprocessext(self, graphnetwork, startid:int, endid: int) -> dict:  # uses graph functionality in the graph network
        geometrydata = gData.GeometryData()
        preprocessed_segments = dict()

        coord_cnt = 0

        graphfuncs = graphfxns.graphfunctions()

        path:list = graphfuncs.getpath(graphnetwork, startid, endid)
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

            linegeom = LineString(reduced_coords_list)
            seg.geometry = linegeom
            seg.lastv = graphfuncs.get_last_v(gdf)
            seg.firstu = graphfuncs.get_first_u(gdf)
            seg.successors = graphfuncs.getpath(graphnetwork, roadid, endid) #(graphnetwork, seg.lastv)  # outgoing segment from the current
            seg.predecessors = graphfuncs.getreversepath(graphnetwork, roadid, startid)  # incoming segment to the current
            seg.length = length
            seg.cumDist = cumdistance
            seg.id = roadid
            seg.nodes = nodes
            seg.setFow(highway)
            seg.setFrc(highway)
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