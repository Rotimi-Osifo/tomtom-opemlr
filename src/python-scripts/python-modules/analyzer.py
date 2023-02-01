from typing import List

import geopandas
import geopy.distance

import RoadNetworkManager as nManager
import roadnetworkgraphsearch
import LineStringData

import filterfunctions
import barefootoutput
import segment
import fileutilities
import trajectorybuilder
import trajectory

from geopy.distance import geodesic

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
        file_utilities = fileutilities.fileutilities()
        barefootoutjsondata = file_utilities.getbarefootoutput(keyfordataset)
        return barefootoutput.getoutputasflattenedlatfirst(barefootoutjsondata)

    def get_barefoot_output_coordinates_lng_first(self, keyfordataset: int) -> list: # coordinates_name = barefootoutput.coordinates_*
        file_utilities = fileutilities.fileutilities()
        barefootoutjsondata = file_utilities.getbarefootoutput(keyfordataset)
        return barefootoutput.getoutputasflattenedlngfirst(barefootoutjsondata)

    def getdecodertrajectorycoordinates(self, keyfordataset: int) -> list:

        file_utilities = fileutilities.fileutilities()
        dekoderoutputjson = file_utilities.getdecoderoutput(keyfordataset)

        lineStringData = LineStringData.LineStringData()
        lineStringData.get_linestring_from_wkt_strings(dekoderoutputjson)

        return lineStringData.all_coords_from_wkt

    def getdecodertrajectorycoordinates_lng_first(self, keyfordataset: int) -> list:

        file_utilities = fileutilities.fileutilities()
        dekoderoutputjson = file_utilities.getdecoderoutput(keyfordataset)

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

    def buildbase_data_with_list(self, maingraphnetwork: geopandas, reflist: list) -> geopandas:
        filterfxns = filterfunctions.filterfunctions()
        return filterfxns.filterRoadNetworkWithRef(maingraphnetwork, reflist)

    def buildbase_data_for_network(self, maingraphnetwork: geopandas, reflist: list) -> geopandas:
        filterfxns = filterfunctions.filterfunctions()
        return filterfxns.filterRoadNetworkWithRefAndName(maingraphnetwork, reflist)

    def build_visited_set(self,  test_graph: geopandas):
        roadNetworkManager_graph_builder: nManager.RoadNetworkManager = nManager.RoadNetworkManager()
        return roadNetworkManager_graph_builder.buidConnectedSegmentsFromGraph(test_graph)

    def build_path(self,  test_graph: geopandas, trajectory_store_key: int) -> list:
        roadnetworkgraphsearchloc = roadnetworkgraphsearch.roadnetworkgraphsearch()
        roadnetworkgraphsearchloc.buildconnectedsegmentsext(test_graph, trajectory_store_key)
        trajectoriestore:dict = roadnetworkgraphsearchloc.trajectoriesstore
        trajectory_:dict = trajectoriestore[trajectory_store_key]
        trajectory_start_segment: segment.segment = trajectory_[trajectory_store_key]

        trajectory_path_list:list = list(trajectory_start_segment.successors)
        trajectory_path_list.insert(0, trajectory_store_key)
        return trajectory_path_list

    def build_pathext(self, graphnetwork: geopandas, startid: int, endid: int, direction: int, highwayref: str,
                      name: str) -> trajectory.trajectory:

        trajectorybuilderloc: trajectorybuilder.trajectorybuilder = trajectorybuilder.trajectorybuilder()
        return trajectorybuilderloc.buildpathbyhighwayref(graphnetwork, startid, endid, direction, highwayref, name)

    def get_visited_set_for_key_set(self, \
                                    roadnetwork_graphsearch: roadnetworkgraphsearch.roadnetworkgraphsearch,\
                                    keyfordataset: int) -> list:

        datastore = roadnetwork_graphsearch.datastore
        return datastore[keyfordataset]

    def write_data_file_for_vehicle_client(self, coordinates: list):
        file_utilities = fileutilities.fileutilities()
        file_utilities.write_data_file_for_vehicle_client(coordinates)

    def get_distance_between(self, first, second):
        geopy.location.Location.
        return geodesic(first, second).m

    def calculate_distances(self):

        start_lat: float = 57.708870
        start_lng: float = 11.974560
        tolerances: List = [1E-1, 1E-2, 1E-3, 1E-4, 1E-5, 1E-6, 1E-7, 1E-8, 1E-9, 1E-10, 1E-11]

        for tolerance in tolerances:

            first = (start_lat, start_lng)

            end_lat : float= start_lat + tolerance
            end_lng : float= start_lng + tolerance
            second = (end_lat, end_lng)

            distance = self.get_distance_between(first, second)
            print("(start_lat: , start_lng: ) = ", "(", start_lat, start_lng, ")", "epsilon in degrees = ", tolerance,  "(end_lat: , end_lng: ) = ", "(",
                  end_lat, end_lng, ")", "distance in metres = ", distance)

    def find_diff(self, first: list, second: list):
        idx: int = 0
        while idx < len(first):
            first_point = first[idx]
            second_point = second[idx]

            distance = self.get_distance_between((first_point[1], first_point[0]), (second_point[1], second_point[0]))
            print("first coordinate: ", "(", first_point[0], first_point[1], ")", "second coordinate: ", "(", second_point[0], second_point[1], ")")
            print("lng diff: ", abs(first_point[0] - second_point[0]), "lat diff: ", abs(first_point[1] - second_point[1]), "distance: ", distance)
            idx = idx + 1