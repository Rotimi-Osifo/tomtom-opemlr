import EnrichedCoordinate
import shapely.wkt
class  EnrichedCoordinates:
    def __init__(self):
        self.enrichedCoordinates = list()

    def getEnrichedCoordinates(selfself, target_search_network, networkId):
        gdf = target_search_network[target_search_network['id'].isin([networkId])]
        dist = 0;
        print(gdf)
        u = gdf.u
        for road in gdf.itertuples():
            geom_str = str(road.geometry)
            geometry = shapely.wkt.loads(geom_str)
            geom = geometry.coords
            enrichedCoordinate = EnrichedCoordinate.EnrichedCoordinate()
            for point in geom:
                enrichedCoordinate.long = point[0]
                enrichedCoordinate.lat = point[1]
            dist = dist + road.length
            enrichedCoordinate.dist = dist







