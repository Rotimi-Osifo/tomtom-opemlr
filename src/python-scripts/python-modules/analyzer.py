import RoadNetworkManager as nManager
import roadnetworkgraphsearch
import LineStringData

from testdataselector import TestDataSelector

class analyzer:
    def __init__(self):
        self.data_matrix = None
        self.roadnetwork_graphsearch: roadnetworkgraphsearch.roadnetworkgraphsearch = None


    def doanalysis(self, graphnetwork):
        roadNetworkManager_graph_builder = nManager.RoadNetworkManager()
        self.roadnetwork_graphsearch = roadNetworkManager_graph_builder.buidConnectedSegmentsFromGraph(graphnetwork)

    def get_visited_set_for_key_set(self, keyfordataset):
        if self.roadnetwork_graphsearch is not None:
            datastore = self.roadnetwork_graphsearch.datastore
            return datastore[keyfordataset]
        return None

    def create_barefoot_test_set(self, graphnetwork, keyfordataset):
        if self.roadnetwork_graphsearch is not None:
            datastore = self.roadnetwork_graphsearch.datastore
            visitedset = datastore[keyfordataset]
            testdataselector_barefoot = TestDataSelector()
            testdataselector_barefoot.create_barefoot_data_from_list(visitedset, graphnetwork)

    def get_barefoot_output_coordinates_lat_first(self, coordinates_name) -> list: # coordinates_name = barefootoutput.coordinates_*
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

    def get_input_data_for_analysis(self, graphnetwork, keyfordataset):
        if self.roadnetwork_graphsearch is not None:
            datastore = self.roadnetwork_graphsearch.datastore
            visitedset = datastore[keyfordataset]

            lineStringData = LineStringData.LineStringData()
            lineStringData.get_linestring_from_ids(graphnetwork, visitedset)

            return lineStringData.all_coords_from_ids




