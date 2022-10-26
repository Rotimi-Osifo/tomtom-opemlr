

def create_road_network_from_id(segmentid, target_search_network):
     return target_search_network[target_search_network['id'].isin([segmentid])]

def checkNextOrPreviousGeometry(these_coordinates, those_coordinates, geometryData):
    for this_point in these_coordinates:
        for that_point in those_coordinates:
            if geometryData.pointsAreEqual(this_point, that_point) == True:
                return True
    return False

def findNextNeighBour(current_id, current_coordinates, geometryData, roadNetwork, target_search_network):
    geometry_type =  geometryData.geometry_types[0]
    neighbours = list()
    for road in target_search_network.itertuples():
        that_id = road.id
        that_geom = geometryData.get_line_string(road.geometry)
        those_coordinates = geometryData.getCoordinates(that_geom, geometry_type)
        if that_id != current_id:
            if  checkNextOrPreviousGeometry(current_coordinates, those_coordinates,  geometryData) == True:
                if geometryData.referenceIds.count(that_id) >= 1:
                    neighbours.append(that_id)
    return neighbours

def findNeighBoursFromNetwork(geometryData, roadNetwork,  target_search_network):
    neighbours_container = dict()
    
    geometry_type =  geometryData.geometry_types[0]
    for road in roadNetwork.itertuples():
        this_id = road.id
        this_geom = geometryData.get_line_string(road.geometry)
        these_coordinates = geometryData.getCoordinates(this_geom, geometry_type)
        nextOrPreviousId = findNextNeighBour(this_id, these_coordinates, geometryData, roadNetwork,  target_search_network)
        
        if len(nextOrPreviousId) >= 1:
            neighbours_container[this_id] = nextOrPreviousId
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

