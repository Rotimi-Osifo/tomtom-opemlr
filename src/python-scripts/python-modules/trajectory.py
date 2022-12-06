import geopandas

import trajectorydata
import roadnetworkgraphsearch
import segment

class trajectory:

    def __init__(self):
        self.trajectoryData = None
        self.path: list = None

    def buildpathbyhighwayref(self,  graphnetwork: geopandas, startid:  int, endid: int, direction: int, highwayref: str) -> list:
        geojsonfilename: str = "map_data_as_geojson_" + str(startid),
        self.trajectoryData = trajectorydata.trajectorydata(startid, direction,  geojsonfilename,  highwayref, endid)

        roadnetworkgraphsearchloc = roadnetworkgraphsearch.roadnetworkgraphsearch()
        roadnetworkgraphsearchloc.buildconnected_segments(graphnetwork, self.trajectoryData)

        trajectoriestore: dict = roadnetworkgraphsearchloc.trajectoriesstore
        trajectory_: dict = trajectoriestore[startid]
        trajectory_start_segment: segment.segment = trajectory_[startid]

        trajectory_path_list: list = list(trajectory_start_segment.successors)
        trajectory_path_list.insert(0, startid)

        self.path = trajectory_path_list

        return self.path