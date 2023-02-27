import GeometryData as gdata
import neighbour_search as nb_s
from trajectorydata import trajectorydata
import shapely.wkt as shwkt
import GeometryData as gData

import sys, json, geojson, datetime;
from datetime import datetime
from datetime import timedelta
import json

import CummulativeDistanceAndTime

class TestDataSelector:
    def __init__(self):
        self.idsLists = dict()

    def getstartdata(self):
        startdatalist = list()

        startdatalistloc = trajectorydata(4040302, 1)
        startdatalist.append(startdatalistloc)
        startdatalistloc = trajectorydata(284402024, 2)
        startdatalist.append(startdatalistloc)
        startdatalistloc = trajectorydata(237772646, 1)
        startdatalist.append(startdatalistloc)
        startdatalistloc = trajectorydata(237772647, 2)
        startdatalist.append(startdatalistloc)

        return  startdatalist

    def fix_max_speed(self, graphnetwork):
        network_graph = CummulativeDistanceAndTime.fixNAForMaxSpeed(graphnetwork)
        network_graph = CummulativeDistanceAndTime.replaceNAInMaxSpeed(network_graph)

        return network_graph

    def get_and_store_test_data(self, targetNetwork, mainNetwork):
        geometryData = gdata.GeometryData()
        startdatalist = self.getstartdata()
        for startdata in startdatalist:
            idList = list()
            startIdList = [startdata.roadid]
            nb_s.getCloseNeighBoursFromRoadNetwork(geometryData, \
                                                    targetNetwork, \
                                                    mainNetwork, \
                                                    startIdList, \
                                                    idList)

            self.idsLists[startdata.roadid] = idList

    def create_barefoot_data_from_listext(self, idsList, graphroadnetwork, trajectory_identifier: str):
        geometrydata = gData.GeometryData()
        graphnetwork = self.fix_max_speed(graphroadnetwork)
        lines_as_single = list()
        timestamp = datetime.utcnow()
        dist = 0
        prev = [0.0, 0, 0]

        delta = timedelta(seconds=8)
        for roadid in idsList:
            gdf = graphnetwork[graphnetwork['id'].isin([roadid])]
            coords_list = list()
            time_list = list()
            for road in gdf.itertuples():

                dist = dist + road.length
                speed_m_per_secs = (1000.0 * road.maxspeed) / 3600
                travel_time = (dist / speed_m_per_secs)




                geom_str = str(road.geometry)
                geometry = shwkt.loads(geom_str)
                geom = geometry.coords

                for point in geom:
                    coords_list.append((point[0], point[1]))
                    time_list.append(timestamp)
                reduced_coords_list = list()
            for coord in coords_list:
                if not geometrydata.pointsAreEqual(coord, prev):
                    reduced_coords_list.append(coord) # no duplicate of
                prev = coord

            idx = 0

            for coord in reduced_coords_list:
                timestamp = (timestamp + delta)
                print(road.id, " ", delta, " ", travel_time, " ", speed_m_per_secs, " ", road.length, " ", dist, " ",
                      timestamp)
                point = "POINT(" + str(coord[0]) + " " + str(coord[1]) + ")"
                datapoint = {
                    "point": point,
                    "time": timestamp.strftime("%Y-%m-%d %H:%M:%S%Z") + "+0000",
                    "id": "\\x0001"
                }
                lines_as_single.append(datapoint)
                idx = idx + 1

        data_path = "../../../data/"
        file_name = data_path + "road_" + "barefoot_data_" + trajectory_identifier + ".geojson"
        # output = json.dumps(lines_as_single, separators=(',', ':'))
        with open(file_name, 'w') as f:
            json.dump(lines_as_single, f, separators=(',', ':'))
            f.close()









