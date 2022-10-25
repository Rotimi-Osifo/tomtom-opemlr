class SearchData:
    def __init__(self):
        self.ordered_sequence = list()
    
    def addToList(self, value):
        self.ordered_sequence.append(value)

def create_road_network_from_id(segmentid, target_search_network):
     return target_search_network[target_search_network['id'].isin([segmentid])]


def insertNext(neighbours_key_values, key, searchData):
    neighbours = neighbours_key_values[key]
    if searchData.ordered_sequence.count(key) == 0:
        if len(neighbours) == 1:
            searchData.addToList(key)
            nb = neighbours[0]
            if searchData.ordered_sequence.count(nb):
                searchData.addToList(nb)
                insertNext(neighbours_key_values, nb, searchData)
        elif len(neighbours) == 2:
            if searchData.ordered_sequence.count(neighbours[0]) == 0:
                searchData.addToList(neighbours[0])
                insertNext(neighbours_key_values, neighbours[0], searchData)
            else:
                searchData.addToList(neighbours[1])
                insertNext(neighbours_key_values, neighbours[1], searchData)

def extractOrderedSequenceOfRoads(neighbours_key_values):
    searchData = SearchData()
    keys = neighbours_key_values.keys();

    for key in keys:
        


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
                if geometryData.targetIds.count(that_id) >= 1:
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
