import geopandas

import RoadNetworkManager as nManager
import roadnetworkgraphsearch
import LineStringData

import filterfunctions
import barefootoutput

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

    def get_barefoot_output_coordinates_lat_first(self, keyfordataset: int) -> list: # coordinates_name = barefootoutput.coordinates_*
        barefoot_coordinates = barefootoutput.getbarefootcoordinatesfortrajectory(keyfordataset)
        barefootroads = list()
        for segmenttupples in coordinates_name:
            for point in segmenttupples:
                barefootroads.append((point[1], point[0])) #lat first for folium map
        return barefootroads

    def get_barefoot_output_coordinates_lng_first(self, coordinates_name) -> list: # coordinates_name = barefootoutput.coordinates_*
        barefootroads = list()
        for segmenttupples in coordinates_name:
            for point in segmenttupples:
                barefootroads.append((point[0], point[1])) #lat first for folium map
        return barefootroads

    def get_input_data_for_analysis(self, graphnetwork: geopandas, \
                                    roadnetwork_graphsearch: roadnetworkgraphsearch.roadnetworkgraphsearch, \
                                    keyfordataset: int):
        datastore = roadnetwork_graphsearch.datastore
        visitedset = datastore[keyfordataset]

        lineStringData = LineStringData.LineStringData()
        lineStringData.get_linestring_from_ids(graphnetwork, visitedset)

        return lineStringData.all_coords_from_ids

    def buildbase_data(self,  maingraphnetwork: geopandas, highwayref: str)-> geopandas:
        filterfxns = filterfunctions.filterfunctions()
        return filterfxns.filterRoadNetworkWithRef(maingraphnetwork, [highwayref])

    def build_visited_set(self,  test_graph: geopandas):
        roadNetworkManager_graph_builder: nManager.RoadNetworkManager = nManager.RoadNetworkManager()
        return roadNetworkManager_graph_builder.buidConnectedSegmentsFromGraph(test_graph)

    def get_visited_set_for_key_set(self, \
                                    roadnetwork_graphsearch: roadnetworkgraphsearch.roadnetworkgraphsearch,\
                                    keyfordataset: int) -> list:

        datastore = roadnetwork_graphsearch.datastore
        return datastore[keyfordataset]



