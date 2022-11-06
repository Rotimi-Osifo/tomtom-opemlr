import ConnectedLinesData as connData

import connectedsegments as connSegments

import CummulativeDistanceCalculator

import startdata

def create_road_network_from_id(segmentid, target_search_network):
     return target_search_network[target_search_network['id'].isin([segmentid])]

def checkNextOrPreviousGeometry(these_coordinates, those_coordinates, geometryData):
    for this_point in these_coordinates:
        for that_point in those_coordinates:
            if geometryData.pointsAreEqual(this_point, that_point) == True:
                return True
    return False

def checkNextOrPreviousGeometryExt(these_coordinates, those_coordinates, geometryData, lineData):
    for this_point in these_coordinates:
        for that_point in those_coordinates:
            if geometryData.pointsAreEqual(this_point, that_point) == True:
                lineData.setConnectionPoint(this_point)
                return True
    return False

def findNextNeighBourExt(current_id, current_coordinates, geometryData, target_search_network, connectedSegmentData):
    geometry_type =  geometryData.geometry_types[0]

    lineData = connData.LineData()
    for road in target_search_network.itertuples():
        that_id = road.id
        that_geom = geometryData.get_line_string(road.geometry)
        those_coordinates = geometryData.getCoordinates(that_geom, geometry_type)
        if that_id != current_id:
            if  checkNextOrPreviousGeometryExt(current_coordinates, those_coordinates,  geometryData, lineData) == True:
                lineData.setCurrentSegmentId(current_id)
                lineData.setConnectedSegmentId(that_id)
                lineData.setConnectedSegmentIsBefore(False)
                lineData.setCurrentSegmentIsBefore(True)
                connectedSegmentData.addToLinesData(lineData)
    return connectedSegmentData

def findNextNeighBour(current_id, current_coordinates, geometryData, target_search_network):
    geometry_type =  geometryData.geometry_types[0]
    neighbours = list()
    for road in target_search_network.itertuples():
        that_id = road.id
        that_geom = geometryData.get_line_string(road.geometry)
        those_coordinates = geometryData.getCoordinates(that_geom, geometry_type)
        if that_id != current_id:
            if  checkNextOrPreviousGeometry(current_coordinates, those_coordinates,  geometryData) == True:
                neighbours.append(that_id)
    return neighbours

def findConnectedSegments(geometryData, roadNetwork,  target_search_network, startId):
    connectedSegments = connSegments.ConnectedSegments()
    connectedSegments.addToUnsortedConnectedLines(roadNetwork)
    refSize = len(connectedSegments.unsortedConnectedSegments)

    return findNeighBoursFromNetworkList(geometryData, roadNetwork,  target_search_network, startId, refSize, connectedSegments)

def findNeighBoursFromNetworkList(geometryData, roadNetwork,  target_search_network, startId, refSize, connectedSegments):

    print(connectedSegments.sortedConnectedSegments)
    geometry_type =  geometryData.geometry_types[0]
    this_id = startId
    if len(connectedSegments.sortedConnectedSegments) < refSize:
        connectedLinesData =  connData.ConnectedLinesData()
        rawGeometry = connectedSegments.unsortedConnectedSegments[this_id]
        this_geom = geometryData.get_line_string(rawGeometry)
        these_coordinates = geometryData.getCoordinates(this_geom, geometry_type)
        connectedLinesData_r = findNextNeighBourExt(this_id, these_coordinates, geometryData, target_search_network, connectedLinesData)
        
        if len(connectedLinesData_r.linesData) >= 1:
            for  lineData in connectedLinesData_r.linesData:
                if connectedSegments.sortedConnectedSegments.count(lineData.currentSegmentId) == 0:
                    connectedSegments.addToSortedConnectedLines(lineData.currentSegmentId)
                if connectedSegments.sortedConnectedSegments.count(lineData.connectedSegmentId) == 0:
                    connectedSegments.addToSortedConnectedLines(lineData.connectedSegmentId)
                    findNeighBoursFromNetworkList(geometryData, roadNetwork,  target_search_network, lineData.connectedSegmentId, refSize, connectedSegments)
            findNeighBoursFromNetworkList(geometryData, roadNetwork,  target_search_network, this_id, refSize, connectedSegments)        
    else:
        return connectedSegments


def findCloseNeighBoursFromNetwork(geometryData, roadNetwork, target_search_network):
    startIdList = [4040302]
    idList = list()
    neighbours_container = dict()
    cumDistanceList = 0
    return findCloseNeighBoursFromNetworkExt(geometryData, roadNetwork, target_search_network, startIdList, idList,
                                      neighbours_container,  cumDistanceList)

def findCloseNeighBoursFromNetworkExt(geometryData, roadNetwork, target_search_network, startIdList,  idList, neighbours_container,  cumDistanceList):
    geometry_type = geometryData.geometry_types[0]
    print(idList)
    if len(idList) <= len(roadNetwork):

        for this_id in startIdList:
            if idList.count(this_id) == 0:
                cumDistanceList = cumDistanceList + CummulativeDistanceCalculator.calculateCummulativeDistance(this_id, target_search_network)
                idList.append(this_id)
                neighbours_container[this_id] = cumDistanceList
                gdf = target_search_network[target_search_network['id'] == this_id]
                for road in gdf.itertuples():
                    this_geom = geometryData.get_line_string(road.geometry)
                    these_coordinates = geometryData.getCoordinates(this_geom, geometry_type)
                    nextOrPreviousId = findNextNeighBour(this_id, these_coordinates, geometryData, target_search_network)

                    if len(nextOrPreviousId) >= 1:
                        findCloseNeighBoursFromNetworkExt(geometryData, roadNetwork, target_search_network,  nextOrPreviousId,  idList, neighbours_container,  cumDistanceList)
    return neighbours_container

def findCloseNeighBoursFromRoadNetwork(geometryData, roadNetwork, target_search_network, startIdList, idList):
    geometry_type = geometryData.geometry_types[0]
    print(idList)
    if len(idList) <= len(roadNetwork):

        for this_id in startIdList:
            if idList.count(this_id) == 0:
                idList.append(this_id)
                gdf = target_search_network[target_search_network['id'] == this_id]
                for road in gdf.itertuples():
                    this_geom = geometryData.get_line_string(road.geometry)
                    these_coordinates = geometryData.getCoordinates(this_geom, geometry_type)
                    nextOrPreviousId = findNextNeighBour(this_id, these_coordinates, geometryData, target_search_network)

                    if len(nextOrPreviousId) >= 1:
                        findCloseNeighBoursFromRoadNetwork(geometryData, roadNetwork, target_search_network, nextOrPreviousId, idList)
    return idList

def findNeighBoursFromNetwork(geometryData, roadNetwork,  target_search_network):
    neighbours_container = dict()
    idList = list()
    geometry_type =  geometryData.geometry_types[0]
    for road in roadNetwork.itertuples():
        if idList.count(road.id) == 0:
            this_id = road.id
            cumDistanceList = CummulativeDistanceCalculator.calculateCummulativeDistance(road.id, target_search_network)
            idList.append(road.id)
        #this_geom = geometryData.get_line_string(road.geometry)
        #this_geom = geometryData.get_line_string_shapely(road.geometry)
        #these_coordinates = geometryData.getCoordinates(this_geom, geometry_type)
        #nextOrPreviousId = findNextNeighBour(this_id, these_coordinates, geometryData, target_search_network)
        
        #if len(nextOrPreviousId) >= 1:
        #    neighbours_container[this_id] = nextOrPreviousId
    return neighbours_container

def getNextOrPreviousLine(these_coordinates, this_id, those_features,  geometry_type, geometryData):
    neighbours = list()
    for that_feature in those_features:
        that_props = that_feature['properties'] 
        that_id = that_props['id']
        that_geom = that_feature['geometry']
        those_coordinates =  geometryData.getCoordinates(that_geom, geometry_type)
        if this_id != that_id:
            if checkNextOrPreviousGeometry(these_coordinates, those_coordinates, geometryData) == True:
                neighbours.append(that_id)
    return neighbours

def findNeighBoursFromCollection(collection, geometryData, geometry_type):
    neighbours_container = dict()
    
    features = collection['features']
    for this_feature in features:
        this_props = this_feature['properties'] 
        this_id = this_props['id']
        this_geom = this_feature['geometry']
        these_coordinates = geometryData.getCoordinates(this_geom, geometry_type)
        nextOrPrevious = getNextOrPreviousLine(these_coordinates, this_id, features, geometry_type, geometryData)
        
        if len(nextOrPrevious) >= 1:
            neighbours_container[this_id] = nextOrPrevious
    return neighbours_container

def extractOrderedSequenceOfRoads(startId, neighbours_key_values, geometryData):
    key = startId
    if len(geometryData.targetIds) <= geometryData.referenceSize:
        if key in neighbours_key_values:
            neighbours = neighbours_key_values[key]
            if geometryData.targetIds.count(key) == 0:
                if len(neighbours) == 1:
                    nb = neighbours[0]
                    if len(geometryData.targetIds) == 0 or geometryData.targetIds.count(nb) == 0:
                        geometryData.addToTargetIds(key)
                        geometryData.addToTargetIds(nb)
                        extractOrderedSequenceOfRoads(nb, neighbours_key_values, geometryData)
                elif len(neighbours) == 2:
                    if  geometryData.targetIds.count(neighbours[0]) == 0:
                        geometryData.addToTargetIds(neighbours[0])
                        extractOrderedSequenceOfRoads(neighbours[0], neighbours_key_values, geometryData)
                    else:
                        geometryData.addToTargetIds(neighbours[1])
                        extractOrderedSequenceOfRoads(neighbours[1], neighbours_key_values, geometryData)
                else:
                    for id in neighbours:
                        if  geometryData.targetIds.count(id) == 0:
                            geometryData.addToTargetIds(id)
                            extractOrderedSequenceOfRoads(id, neighbours_key_values, geometryData)

            else:
                if len(neighbours) == 1:
                    nb = neighbours[0]
                    if len(geometryData.targetIds) == 0 or geometryData.targetIds.count(nb) == 0:
                        geometryData.addToTargetIds(key)
                        geometryData.addToTargetIds(nb)
                        extractOrderedSequenceOfRoads(nb, neighbours_key_values, geometryData)
                elif len(neighbours) == 2:
                    if  geometryData.targetIds.count(neighbours[0]) == 0:
                        geometryData.addToTargetIds(neighbours[0])
                        extractOrderedSequenceOfRoads(neighbours[0], neighbours_key_values, geometryData)
                    else:
                        geometryData.addToTargetIds(neighbours[1])
                        extractOrderedSequenceOfRoads(neighbours[1], neighbours_key_values, geometryData)
                else:
                    for id in neighbours:
                        if  geometryData.targetIds.count(id) == 0:
                            geometryData.addToTargetIds(id)
                            extractOrderedSequenceOfRoads(id, neighbours_key_values, geometryData)
    else:
        return geometryData.targetIds

