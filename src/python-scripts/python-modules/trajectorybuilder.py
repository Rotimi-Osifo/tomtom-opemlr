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
