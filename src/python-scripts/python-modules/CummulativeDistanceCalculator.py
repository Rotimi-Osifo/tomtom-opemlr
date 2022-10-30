
def calculateCummulativeDistanceExt(roadId, targetSearchNetwork):
    gdf = targetSearchNetwork[targetSearchNetwork['id'] == roadId]
    cumDistanceList = list()
    length = 0;
    for road in gdf.itertuples():
        length = length + road.length
        cumDistanceList.append(length)
        print("road id -: ", road.id, "u-: ", road.u, "v-: ", road.v, "length -: ", length, "cum length -: ", road.length)

    return cumDistanceList

def calculateCummulativeDistance(roadId, targetSearchNetwork):
    gdf = targetSearchNetwork[targetSearchNetwork['id'] == roadId]
    length = 0;
    for road in gdf.itertuples():
        length = length + road.length
        #print("road id -: ", road.id, "length -: ", length, "cum length -: ", road.length)

    return length
