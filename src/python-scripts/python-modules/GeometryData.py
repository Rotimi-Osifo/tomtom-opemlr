# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 12:54:57 2022

@author: OOSIFO
"""
from geojson import LineString
from geojson import MultiLineString

class GeometryData:
    def __init__(self):
        self.epsilon = 0.000000000000000005
        self.geometry_types = ['geojson.geometry.LineString', \
                               'shapely.geometry.linestring.LineString']
        self.targetIds = list()
        self.referenceIds = list()
        self.referenceSize = None
    
    def setReferenceSize(self, referenceSize):
        self.referenceSize = referenceSize
        
    def addToTargetIds(self, roadid):
        if self.targetIds.count(roadid) == 0:
            self.targetIds.append(roadid)

    def setReferenceIds(self, roadNetwork):
        for road in roadNetwork.itertuples():
            if self.referenceIds.count(road.id) == 0:
                self.referenceIds.append(road.id)
         
    def isDuplicate(self, current_point, prev_point):
        return self.pointsAreEqual(current_point, prev_point)

    def pointsAreEqual(self, this_point, that_point):
        if (abs(this_point[0] - that_point[0]) < self.epsilon and \
            abs(this_point[1] - that_point[1]) < self.epsilon):
            return True
        return False
    
    def getCoordinates(self, geometry, geometry_type):
        if geometry_type == 'geojson.geometry.LineString':
            return geometry['coordinates']
        elif geometry_type == 'shapely.geometry.linestring.LineString':
            return geometry.coords
        return None

    def get_line_string(self, multi_line: MultiLineString) -> LineString:

        line_list = list()
        prev_point = [0.0, 0.0]
        for line in multi_line.geoms:

            for point in line.coords:
                if self.isDuplicate(point, prev_point) == False:
                    line_list.append((point[0], point[1]))
                    prev_point = point
        line_list.sort(key=lambda p: p[0])
        return LineString(line_list)

    def get_line_string_shapely(self, shapelyLinstrings) -> LineString:
        line_list = list()
        for geom in list(shapelyLinstrings):
            for point in list(geom.coords):
                line_list.append((point[0], point[1]))
        return LineString(line_list)

