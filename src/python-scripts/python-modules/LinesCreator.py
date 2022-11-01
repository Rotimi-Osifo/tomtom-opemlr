import Node as nd
import Line as ln
import Lines as lns


class LinesCreator:
    def __init__(self):
        self.lines = None
    
    def createLines(self, idList, geometryData, targetNetwork):
        lines = lns.Lines()
        coord_cnt = 1
        for roadId in idList:
            gdf_loc = targetNetwork[targetNetwork['id'].isin([roadId])]
        
            line = ln.Line()
            line.setStartNodeId(coord_cnt)
            for road in gdf_loc.itertuples():
                geom = geometryData.get_line_string(road.geometry)
                coordinates = geom['coordinates']
                line.setGeometry(geom)
                line.setHighway(road.highway)
                line.setRoadId(int(road.id))
                line.setLength(int(road.length))
                line.setFrc(road.highway)
                line.setFow(road.highway)

                coordinates.sort(key = lambda p: p[0])

                for point in coordinates:

                    node = nd.Node()
                    node.setCoordinate(point)
                    node.setNodeId(coord_cnt)
                    node.setRoadId(int(road.id))
                    node.setnodeLink(road.id)
                    
                    line.addNode(node)

                    coord_cnt = coord_cnt + 1
                line.setEndNodeId(coord_cnt - 1)
                line.setDirection(int(1))
                lines.addLine(road.id, line)
        self.lines = lines
        return lines
    

            
    
        
        
        
        
        


