import geopandas

import RoadNetworkManager as nManager
import roadnetworkgraphsearch
import LineStringData

import filterfunctions
import barefootoutput
import dekoderoutput
import segment

from testdataselector import TestDataSelector

class analyzer:
    def __init__(self):
        self.data_matrix = None
        self.roadnetwork_graphsearch: roadnetworkgraphsearch.roadnetworkgraphsearch = None


    def doanalysis(self, graphnetwork):
        roadNetworkManager_graph_builder = nManager.RoadNetworkManager()
        self.roadnetwork_graphsearch = roadNetworkManager_graph_builder.buidConnectedSegmentsFromGraph(graphnetwork)

    def build_barefoot_test_set(self, graphnetwork: geopandas,  visitedset: list) -> None:
        testdataselector_barefoot = TestDataSelector()
        testdataselector_barefoot.create_barefoot_data_from_list(visitedset, graphnetwork)

    def build_barefoot_test_setext(self, graphnetwork: geopandas, trajectory_path_list: list, trajectory_identifier: str) -> None:
        testdataselector_barefoot = TestDataSelector()
        testdataselector_barefoot.create_barefoot_data_from_listext(trajectory_path_list, graphnetwork, trajectory_identifier)

    def get_barefoot_output_coordinates_lat_first(self, keyfordataset: int) -> list: # coordinates_name = barefootoutput.coordinates_*
        return barefootoutput.get_output_as_flattened_lat_first(keyfordataset)

    def get_barefoot_output_coordinates_lng_first(self, keyfordataset: int) -> list: # coordinates_name = barefootoutput.coordinates_*
        return barefootoutput.get_output_as_flattened_lng_first(keyfordataset)

    def getdecodertrajectorycoordinates(self, keyfordataset: int) -> list:
        dekoderoutputjson = dekoderoutput.getdecodertrajectorycoordinates(keyfordataset)

        lineStringData = LineStringData.LineStringData()
        lineStringData.get_linestring_from_wkt_strings(dekoderoutputjson)
        return lineStringData.all_coords_from_wkt

    def getdecodertrajectorycoordinates_lng_first(self, keyfordataset: int) -> list:
        dekoderoutputjson = dekoderoutput.getdecodertrajectorycoordinates(keyfordataset)

        lineStringData = LineStringData.LineStringData()
        lineStringData.get_linestring_from_wkt_strings(dekoderoutputjson)
        return lineStringData.all_coords_from_wkt_lng_first


    def get_input_data_for_analysis(self, graphnetwork: geopandas, \
                                    roadnetwork_graphsearch: roadnetworkgraphsearch.roadnetworkgraphsearch, \
                                    keyfordataset: int):
        datastore = roadnetwork_graphsearch.datastore
        visitedset = datastore[keyfordataset]

        lineStringData = LineStringData.LineStringData()
        lineStringData.get_linestring_from_ids(graphnetwork, visitedset)

        return lineStringData.all_coords_from_ids

    def get_input_data_for_analysisext(self, graphnetwork: geopandas, trajectory_path_list: list):
        lineStringData = LineStringData.LineStringData()
        lineStringData.get_linestring_from_ids(graphnetwork, trajectory_path_list)

        return lineStringData.all_coords_from_ids

    def get_input_data_for_analysis_lng_first(self, graphnetwork: geopandas, \
                                    roadnetwork_graphsearch: roadnetworkgraphsearch.roadnetworkgraphsearch, \
                                    keyfordataset: int):
        datastore = roadnetwork_graphsearch.datastore
        visitedset = datastore[keyfordataset]

        lineStringData = LineStringData.LineStringData()
        lineStringData.get_linestring_from_ids(graphnetwork, visitedset)

        return lineStringData.all_coords_from_ids_lng_first

    def get_input_data_for_analysis_lng_firstext(self, graphnetwork: geopandas, trajectory_path_list: list) -> list:

        lineStringData = LineStringData.LineStringData()
        lineStringData.get_linestring_from_ids(graphnetwork, trajectory_path_list)

        return lineStringData.all_coords_from_ids_lng_first

    def buildbase_data(self,  maingraphnetwork: geopandas, highwayref: str)-> geopandas:
        filterfxns = filterfunctions.filterfunctions()
        return filterfxns.filterRoadNetworkWithRef(maingraphnetwork, [highwayref])

    def build_visited_set(self,  test_graph: geopandas):
        roadNetworkManager_graph_builder: nManager.RoadNetworkManager = nManager.RoadNetworkManager()
        return roadNetworkManager_graph_builder.buidConnectedSegmentsFromGraph(test_graph)

    def build_path(self,  test_graph: geopandas, trajectory_store_key: int) -> list:
        roadnetworkgraphsearchloc = roadnetworkgraphsearch.roadnetworkgraphsearch()
        roadnetworkgraphsearchloc.buildconnectedsegmentsext(test_graph)
        trajectoriestore:dict = roadnetworkgraphsearchloc.trajectoriesstore
        trajectory_:dict = trajectoriestore[trajectory_store_key]
        trajectory_start_segment:segment.segment = trajectory_[trajectory_store_key]
        trajectory_path_list:list = trajectory_start_segment.successors
        trajectory_path_list.insert(0, trajectory_store_key)
        return trajectory_path_list

    def get_visited_set_for_key_set(self, \
                                    roadnetwork_graphsearch: roadnetworkgraphsearch.roadnetworkgraphsearch,\
                                    keyfordataset: int) -> list:

        datastore = roadnetwork_graphsearch.datastore
        return datastore[keyfordataset]



