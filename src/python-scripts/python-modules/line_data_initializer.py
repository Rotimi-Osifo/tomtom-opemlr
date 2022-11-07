import Line
import GeometryData as gData

import shapely.wkt as shwkt

from geojson import LineString


class line_data_initializer:
    def __init__(self):
        self.lines = dict()
    
    def __get_last_v(self, gdf):
        last_v = None
        for seg in gdf.itertuples():
            last_v = seg.v
        return last_v

    def __get_first_u(self, gdf):
        for seg in gdf.itertuples():
            return seg.u
        
    
    def initializelines(self, filtered_graph_network):
        
        geometrydata = gData.GeometryData()

        for road in filtered_graph_network.itertuples():
            length = 0
            
            gdf = filtered_graph_network[filtered_graph_network['id'] == road.id]
            
            coords_list = list()
            for road in gdf.itertuples():
                length = length + (float(road.length))
                geom_str = str(road.geometry)
                geometry = shwkt.loads(geom_str)
                geom = geometry.coords
                

                for point in geom:
                    coords_list.append((point[0], point[1]))
            
            reduced_coords_list = list()
            prev = [0.0, 0,0]
            for coord in coords_list:
                if not geometrydata.pointsAreEqual(coord, prev):
                    reduced_coords_list.append(coord)
                prev = coord

            linegeom = LineString(reduced_coords_list)
            
            line = Line.Line()
            
            line.setGeometry(linegeom)
            line.setHighway(road.highway)
            line.setRoadId(int(road.id))
            line.setLength(length)
            line.setFrc(road.highway)
            line.setFow(road.highway)
            line.setFirstU(int(self.__get_first_u(gdf)))
            line.setLastV(int(self.__get_last_v(gdf)))
            
            self.lines[road.id] = line

        return   self.lines
        

