import geopandas

import shapely.wkt as shwkt
from shapely.geometry import Point

class DrivePath:
    def __init__(self):
        self.ids = list()


    def calculate_line_lengths(self, idsList: list, graphroadnetwork: geopandas):
        for roadid in idsList:
            gdf: geopandas = graphroadnetwork[graphroadnetwork['id'].isin([roadid])]
            #print(gdf)
            for road in gdf.itertuples():
                geom_str = str(road.geometry)
                #print( geom_str)
                geometry = shwkt.loads(geom_str)
                print(road.length)

    def build_drive_path(self, idsList: list, graphroadnetwork: geopandas, speed: float, sampling: float):
        distance_between: float = speed * sampling
        print( distance_between)
        path: list = list()
        cnt: int = 0
        tot:int = 0
        for roadid in idsList:
            gdf: geopandas = graphroadnetwork[graphroadnetwork['id'].isin([roadid])]

            for road in gdf.itertuples():
                tot = tot + 1
                if (road.length) - distance_between > 0:
                    if self.ids.count(roadid) == 0:
                        self.ids.append(roadid)
                        
                    geom_str = str(road.geometry)
                    geometry = shwkt.loads(geom_str)
                    start: Point = geometry.coords[0]

                    if path.count(start) == 0:
                        path.append(start)

                    end: Point = geometry.coords[1]
                    if path.count(end) == 0:
                        path.append(end)
                    cnt = cnt + 1

        print(cnt, " ", tot)
        return path

