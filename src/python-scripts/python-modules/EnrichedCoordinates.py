import EnrichedCoordinate
class  EnrichedCoordinates:
    def __init__(self):
        self.enrichedCoordinates = list()

    def getEnrichedCoordinates(selfself, target_search_network, networkId):
        gdf = target_search_network[target_search_network['id'].isin([networkId])]
        length = 0;
        print(gdf)
        u = gdf.u
        for road in gdf.itertuples():
            geom_list = list(road.geometry)
            for geom in geom_list:
                enrichedCoordinate = EnrichedCoordinate.EnrichedCoordinate()
                for point in list(geom.coords):
                    enrichedCoordinate.long = point[0]
                    enrichedCoordinate.lat = point[1]





