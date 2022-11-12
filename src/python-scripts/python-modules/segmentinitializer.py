import GeometryData as gData
from geojson import LineString
import shapely.wkt as shwkt
from typing import TypedDict

import segment

class segmentdictionarytype(TypedDict):
    roadid: segment.segment

class segmentinitializer:

    def __init__(self):
        self.initialized_segments:segmentdictionarytype

    def __get_last_v(self, gdf):
        last_v = None
        for seg in gdf.itertuples():
            last_v = seg.v
        return last_v

    def __get_first_u(self, gdf):
        for seg in gdf.itertuples():
            return seg.u

    def __getincomingline(self, graphnetwork, lastv):
        for road in graphnetwork.itertuples():
            #gdf = graphnetwork[graphnetwork['u'].isin([lastv])]
            if road.u == lastv:
                return road.id
        return None

    def __getoutgoingline(self, lines: dict, firstu):
        for key in lines.keys():
            line = lines[key]
            if line.lastv is not None:
                if line.lastv == firstu:
                    return line
        return None

    def initialize_segments(self, graphnetwork):
        geometrydata = gData.GeometryData()
        for road in graphnetwork.itertuples():
            seg = segment.segment()

            gdf = graphnetwork[graphnetwork['id'].isin([road.id])]
            coords_list = list()
            for roadloc in gdf.itertuples():
                geom_str = str(roadloc.geometry)
                geometry = shwkt.loads(geom_str)
                geom = geometry.coords
                prev = [0.0, 0, 0]

                for point in geom:
                    coords_list.append((point[0], point[1]))

            reduced_coords_list = list()
            for coord in coords_list:
                if not geometrydata.pointsAreEqual(coord, prev):
                    reduced_coords_list.append(coord)
                prev = coord

            linegeom = LineString(reduced_coords_list)
            seg.geometry= linegeom
            seg.lastv = self.__get_last_v(gdf)
            seg.firstu = self.__get_first_u(gdf)
            seg.outging = self.__getoutgoingline(graphnetwork, seg.lastv)