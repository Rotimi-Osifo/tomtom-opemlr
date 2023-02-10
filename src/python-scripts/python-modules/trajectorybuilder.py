import geopandas

import trajectory
import trajectorydata
import roadnetworkgraphsearch
import segment

class trajectorybuilder:
    def __init__(self):
        pass

    def buildpathbyhighwayref(self,  graphnetwork: geopandas, startid:  int, endid: int, direction: int, highwayref: str, name:str) -> trajectory.trajectory:
        trajectoryloc: trajectory.trajectory = trajectory.trajectory(startid, endid, direction, highwayref, name)

        geojsonfilename: str = "map_data_as_geojson_" + str(startid)
        print("before geojsonfilename-: ", geojsonfilename)
        trajectoryData = trajectorydata.trajectorydata(startid, direction,  geojsonfilename,  highwayref, endid)

        print("after geojsonfilename-: ", trajectoryData.mapfilename)

        roadnetworkgraphsearchloc = roadnetworkgraphsearch.roadnetworkgraphsearch()
        roadnetworkgraphsearchloc.buildconnected_segments(graphnetwork, trajectoryData)

        trajectoriestore: dict = roadnetworkgraphsearchloc.trajectoriesstore
        trajectory_: dict = trajectoriestore[startid]
        trajectory_start_segment: segment.segment = trajectory_[startid]

        trajectory_path_list: list = list(trajectory_start_segment.successors)
        trajectory_path_list.insert(0, startid)

        trajectoryloc.path = trajectory_path_list

        return trajectoryloc

    def build_path_from_connected_paths(self, graphnetwork: geopandas, paths_data: list, path_name:str) -> trajectory.trajectory:

        if len(paths_data) == 1:
            path_data = paths_data[0]
            startid: int = path_data["startid"]
            endid: int = path_data["endid"]
            direction: int = path_data["direction"]
            highwayref: str = path_data["highwayref"]
            name: str = path_data["name"]
            return self.buildpathbyhighwayref(graphnetwork, startid, endid, direction, highwayref, name)

        trajectory_path_list: list = list()
        for path_data in paths_data:
            startid:int = path_data["startid"]
            endid:int = path_data["endid"]
            direction: int = path_data["direction"]
            highwayref: str = path_data["highwayref"]

            geojsonfilename: str = "map_data_as_geojson_" + str(startid)
            print("before geojsonfilename-: ", geojsonfilename)
            trajectoryData = trajectorydata.trajectorydata(startid, direction, geojsonfilename, highwayref, endid)

            print("after geojsonfilename-: ", trajectoryData.mapfilename)

            roadnetworkgraphsearchloc = roadnetworkgraphsearch.roadnetworkgraphsearch()
            roadnetworkgraphsearchloc.buildconnected_segments(graphnetwork, trajectoryData)

            trajectoriestore: dict = roadnetworkgraphsearchloc.trajectoriesstore
            trajectory_: dict = trajectoriestore[startid]
            trajectory_start_segment: segment.segment = trajectory_[startid]

            if trajectory_path_list.count(startid) == 0:
                trajectory_path_list.append(startid)
                for roadid in trajectory_start_segment.successors:
                    if trajectory_path_list.count(roadid) == 0:
                        trajectory_path_list.append(roadid)

        endid:int = self.get_endid(paths_data)
        startid:int = self.get_startid(paths_data)
        trajectoryloc: trajectory.trajectory = trajectory.trajectory(startid, endid, 3, path_name, path_name)
        trajectoryloc.path = trajectory_path_list
        return trajectoryloc

    def get_startid(self, paths_data):
        start_path_data = paths_data[0]
        startid: int = start_path_data["startid"]
        return startid

    def get_endid(self, paths_data):
        end_path_data = paths_data[len(paths_data) - 1]
        endid: int = end_path_data["endid"]
        return endid