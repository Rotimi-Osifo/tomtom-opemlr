import segment
import shapely.wkt

class connectedsegments:
    def __init__(self):
        self.segments = list()

    def get_connected_segments(self, target_search_network, networkIdList):
        dist = 0
        for networkid in networkIdList:
            gdf = target_search_network[target_search_network['id'].isin([networkid])]

            for road in gdf.itertuples():
                dist = dist + road.length
                geom_str = str(road.geometry)
                geometry = shapely.wkt.loads(geom_str)
                geom = geometry.coords

                seg = segment.segment()
                startpoint = geom[0]
                endpoint = geom[1]
                seg.start = [startpoint[0], startpoint[1]]
                seg.end = [endpoint[0], endpoint[1]]
                seg.cumDist = dist
                seg.maxspeed = road.maxspeed
                seg.id = road.id

                speed_m_per_secs = (1000.0 * road.maxspeed) / 3600
                seg.travel_time = (dist / speed_m_per_secs)

                self.segments.append(seg)

    def build_connected_segments(self, graphnetwork):
        pass






