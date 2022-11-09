from geojson import LineString
from geojson import Feature
from geojson import FeatureCollection
import shapely.wkt as shwkt
import GeometryData as gData


class LineStringData:
    def __init__(self):
        self.line_string_from_ids = None
        self.geojson_linestring = None
        self.shapely_wkt_linestring = None
        self.featurecollection_from_shapely = None
        self.featurecollection_from_ids = None
        self.all_coords_from_ids = list()
        self.all_coords_from_wkt = list()
        self.all_coords_from_ids_lng_first = list()
        self.all_coords_from_wkt_lng_first = list()

    def get_linestring_from_ids(self, graphnetwork, idsList):
        geometrydata = gData.GeometryData()

        all_features_list = list()
        all_geom_in_one = list()
        for roadid in idsList:
            gdf = graphnetwork[graphnetwork['id'].isin([roadid])]
            coords_list = list()
            geom_list = list()
            for segment in gdf.itertuples():
                geom_str = str(segment.geometry)
                geometry = shwkt.loads(geom_str)
                geom = geometry.coords

                for point in geom:
                    coords_list.append((point[0], point[1]))

            prev = [0.0, 0, 0]
            for coord in coords_list:
                if not geometrydata.pointsAreEqual(coord, prev):
                    geom_list.append(coord)
                    all_geom_in_one.append(coord)
                    self.all_coords_from_ids.append([coord[1], coord[0]])
                    self.all_coords_from_ids_lng_first.append(coord)
                prev = coord
            line_string_from_ids = LineString(geom_list)
            feature = Feature(geometry=line_string_from_ids, properties={"id": roadid})
            all_features_list.append(feature)
        self.featurecollection_from_ids = FeatureCollection(all_features_list)
        self.line_string_from_ids = LineString(all_geom_in_one)

        return self.line_string_from_ids

    def get_linestring_from_wkt_strings(self, json_data):
        locations = json_data['lineLocation']
        lines = locations['lines']
        all_features_list = list()
        all_geom_in_one = list()
        for line in lines:
            line_id = line['id']
            wkt = line['wkt']
            geometry = shwkt.loads(wkt)
            geom = geometry.coords
            geom_list = list()
            for point in geom:
                geom_list.append((point[0], point[1]))
                all_geom_in_one.append(point)
                self.all_coords_from_wkt.append([point[1], point[0]])
                self.all_coords_from_wkt_lng_first.append(point)
            shapely_wkt_linestring = LineString(geom_list)
            feature = Feature(geometry=shapely_wkt_linestring, properties={"id":line_id})
            all_features_list.append(feature)

        self.featurecollection_from_shapely = FeatureCollection(all_features_list)
        self.shapely_wkt_linestring = LineString(all_geom_in_one)

        return self.shapely_wkt_linestring
