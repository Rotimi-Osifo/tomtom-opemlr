import trajectorydata
import GeometryData as gData
from geojson import LineString
import shapely.wkt as shwkt

import segment

class startdatacreator:

    def __init__(self):
        self.initialized_segments = dict()

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
