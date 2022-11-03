#import shapely.wkt
import GeometryData as gdata
class wktconversion:
    #def __int__(self):

    def __get_wkt_geom(self, geom):
        coordinates = geom['coordinates']
        start = 'LINESTRING('
        end = ')'
        p_str = ''
        s = len(coordinates)
        cnt = 1
        for point in coordinates:
            if cnt < s:
                p_str = p_str + str(point[0]) + ' ' + str(point[1]) + ', '
            else:
                p_str = p_str + str(point[0]) + ' ' + str(point[1])
            cnt = cnt + 1
        lstr = start + p_str + end
        return lstr

    def get_wkt_from_linestrings(self, roadnetwork):
        lines = list()
        geometryData_loc = gdata.GeometryData()
        for road in roadnetwork.itertuples():
            geom = geometryData_loc.get_line_string(road.geometry)
            line = self.__get_wkt_geom(geom)
            linjson = {
                'id': road.id,
                'wkt': line
            }
            lines.append(linjson)
        locations = {
            "lineLocation":
                {
                    "lines": lines
                }
        }

        return locations