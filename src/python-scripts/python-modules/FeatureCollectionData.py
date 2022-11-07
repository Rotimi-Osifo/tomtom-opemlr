# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 15:50:43 2022

@author: OOSIFO
"""
from geojson import FeatureCollection
import shapely.wkt
import json

import constant_data as cData
import GeometryData as gData
import Nodes
import Lines
import Line
import Node

class FeatureCollectionData:
    def __init__(self):
        self.all_features = list()
        self.lines_features = list()
        self.roads = list()
        self.lines_collection = None
        self.all_collection = None
    

    def __nodeFeatureFromNode(self, node: Node.Node):
        coordinates = node.coordinate
        feature = {
            "type": "Feature",
            "properties":{
                "id": node.nodeId
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    coordinates[0],
                    coordinates[1]
                ]
            },
            "node": node.name
        }
        return feature


    def createCollectionsFromLines(self, lines):
        self.all_features.clear()
        self.lines_features.clear()

        for roadId in lines.keys():
            line = lines[roadId]
            nodes = line.nodes

            for node in nodes:
                nodeFeature = self.__nodeFeatureFromNode(node)
                self.all_features.append(nodeFeature) #nodes
    
            line_feature = {
                    "type": "Feature",
                    "properties":{
                        "id": line.roadId,
                        "direction": line.direction,
                        "endId": line.endNodeId,
                        "startId": line.startNodeId,
                        "length": line.length,
                        "frc": line.frc,
                        "fow": line.fow
                        },
                        "geometry": line.geometry,
                        "id": "link-" + str(line.roadId)
                    }
            self.all_features.append(line_feature)
            self.lines_features.append(line_feature)
            self.roads.append(str(line.roadId))
        self.all_collection = FeatureCollection(self.all_features)
        self.lines_collection = FeatureCollection(self.lines_features)

        data_path = "../../../data/"
        self.writeCollection(data_path + "one_way_E6_map.geojson", self.all_collection)

    def __setNodesForRoadSegment(self, segmentline):
        nodes = segmentline.nodes

        print(segmentline.startNodeId, ' ', segmentline.endNodeId)
        startnode = nodes[segmentline.startNodeId]
        startNodeFeature = self.__nodeFeatureFromNode(startnode)
        self.all_features.append(startNodeFeature)

        endnode = nodes[segmentline.endNodeId]
        endNodeFeature = self.__nodeFeatureFromNode(endnode)
        self.all_features.append(endNodeFeature)

    def createCollectionsFromGraphLines(self, lines: Lines.Lines, nodes: Nodes.Nodes):
        geometryData = gData.GeometryData()

        for key in nodes.keys():
            segmentnodes: list = nodes[key]
            for node in segmentnodes:
                n: Node.Node = node
                n.printnode()
                feature = self.__nodeFeatureFromNode(n)
                self.all_features.append(feature)

        for roadId in lines.keys():
            line = lines[roadId] #short lines between successive coordinates

            line_feature = {
                "type": "Feature",
                "properties": {
                    "id": int(roadId),
                    "direction": int(line.direction),
                    "endId": line.endNodeId,
                    "startId": line.startNodeId,
                    "length": int(line.length),
                    "frc": line.frc,
                    "fow": line.fow
                },
                "geometry": line.geometry,
                "id": "link-" + str(line.roadId)
            }
            self.all_features.append(line_feature)
            self.lines_features.append(line_feature)
            self.roads.append(str(line.roadId))

        self.all_collection = FeatureCollection(self.all_features)
        self.lines_collection = FeatureCollection(self.lines_features)

        #print(self.all_collection)
        #data_path = "../../../data/"
        #self.writeCollection(data_path + "one_way_E6_map_graph.geojson", self.all_collection)
        #self.writeCollection(data_path + "one_way_E6_map_graph_json.json", self.all_collection)

    def createCollectionsFromGraphLinesExt(self, lines: Lines.Lines, nodes: Nodes.Nodes, idlist):
        geometryData = gData.GeometryData()

        for roadid in idlist:
            segmentnodes: list = nodes[roadid]
            for node in segmentnodes:
                n: Node.Node = node
                n.printnode()
                feature = self.__nodeFeatureFromNode(n)
                self.all_features.append(feature)

        for roadId in idlist:
            line = lines[roadId] #short lines between successive coordinates

            line_feature = {
                "type": "Feature",
                "properties": {
                    "id": int(roadId),
                    "direction": int(line.direction),
                    "endId": line.endNodeId,
                    "startId": line.startNodeId,
                    "length": int(line.length),
                    "frc": line.frc,
                    "fow": line.fow
                },
                "geometry": line.geometry,
                "id": "link-" + str(line.roadId)
            }
            self.all_features.append(line_feature)
            self.lines_features.append(line_feature)
            self.roads.append(str(line.roadId))

        self.all_collection = FeatureCollection(self.all_features)
        self.lines_collection = FeatureCollection(self.lines_features)

        #print(self.all_collection)
        #data_path = "../../../data/"
        #self.writeCollection(data_path + "one_way_E6_map_graph.geojson", self.all_collection)
        #self.writeCollection(data_path + "one_way_E6_map_graph_json.json", self.all_collection)

    def createCollections(self, road_network, geometryData):
        self.__createFeaturesCollectionsData(road_network, geometryData)
        self.all_collection = FeatureCollection(self.all_features)
        self.lines_collection = FeatureCollection(self.lines_features)
    
    def createCollectionsFromIds(self, idList, geometryData, targetNetwork):
        line_cnt = 0
        self. __createFeaturesCollection(idList, geometryData, targetNetwork)
        self.all_collection = FeatureCollection(self.all_features)
        self.lines_collection = FeatureCollection(self.lines_features)
    

    def createFeaturesCollectionFromJsonLines(self, lines):
        features_list = list()
        for line in lines:
            line_id = line['id']
            wkt = line['wkt']
            geometry = shapely.wkt.loads(wkt)
            props = {
                'id': line_id
            }
            feature = {
                "type": "Feature",
            "properties": props,
            "geometry": geometry
            }
            features_list.append(feature)
        return FeatureCollection(features_list)

    def __nodeFeature(self, points, coord_cnt):
        feature = {
            "type": "Feature",
            "properties":{
                "id": int(coord_cnt)
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    points[0],
                    points[1]
                ]
            },
            "node": "node-"+ str(coord_cnt)  
        }

        return feature
    
    def __createFeaturesCollection(self, idList, geometryData, targetNetwork):
        coord_cnt = 1
        line_cnt = 0
        for roadId in idList:
            gdf_loc = targetNetwork[targetNetwork['id'].isin([roadId])]
            line_cnt = coord_cnt
            for road in gdf_loc.itertuples():
                geom = geometryData.get_line_string(road.geometry)
                coordinates = geom['coordinates']
                for points in coordinates:
                    feature = self.__nodeFeature(points, coord_cnt)

                   

                    self.all_features.append(feature) #nodes
                    coord_cnt = coord_cnt + 1
                line_feature = {
                    "type": "Feature",
                    "properties":{
                        "id": road.id,
                        "direction": 1,
                        "endId": int(coord_cnt),
                        "startId": int(line_cnt),
                        "length": int(road.length),
                        "frc": cData.highway_frc_mapping.get(road.highway, 0), #deafult case 0
                        "fow": cData.highway_fow_mapping.get(road.highway, 7) #deafult case 7
                        },
                        "geometry": geom,
                        "id": "link-" + str(road.id)
                    }
                self.all_features.append(line_feature)
                self.lines_features.append(line_feature)
                self.roads.append(str(road.id))
    
    def __createFeaturesCollectionsData(self, road_network, geometryData):
        
        coord_cnt = 1
        line_cnt = 0
        for road in road_network.itertuples():
            geom = geometryData.get_line_string(road.geometry)
            coordinates = geom['coordinates']
            line_cnt = coord_cnt
            for points in coordinates:
                feature = self.__nodeFeature(points, coord_cnt)
                self.all_features.append(feature) #nodes
                coord_cnt = coord_cnt + 1
            line_feature = {
                "type": "Feature",
                "properties":{
                    "id": int(road.id),
                    "direction": 1,
                    "endId": int(coord_cnt),
                    "startId": int(line_cnt),
                    "length": int(road.length),
                    "frc": cData.highway_frc_mapping.get(road.highway, 0), #deafult case 0
                    "fow": cData.highway_fow_mapping.get(road.highway, 7) #deafult case 7
                },
                "geometry": geom,
                "id": "link-" + str(road.id)
            }
            self.all_features.append(line_feature)
            self.lines_features.append(line_feature)
            self.roads.append(str(road.id))
    
    def writeCollection(self, file_root_path, collection):
        self.__dumpToFile(file_root_path, collection)
            
    def writeLineFeatures(self, file_root_path):
        #road_dir_file_root = "../data/segments/"
        features = self.line_collection
        for feature in features:
            props = feature['properties']
            ref_name = props['id']
            file_name = file_root_path + "road_" + id + ".geojson"
            self.__dumpToFile(file_name, feature)
    
    def writeAllFeatures(self, file_root_path):
        features = self.all_collection
        for feature in features:
            props = feature['properties']
            ref_name = props['id']
            file_name = file_root_path + "road_" + id + ".geojson"
            self.__dumpToFile(file_name, feature)
    
    def __dumpToFile(self, file_name, feature):
        print(file_name)
        with open(file_name,'w') as f:
            json.dump(feature, f, separators=(',', ':'))
            f.close()
        