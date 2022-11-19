import geopandas as geopandas


class graphfunctions:
    def __init__(selfself):
        pass

    def get_last_v(self, gdf: geopandas) -> int: # uses graph functionality in the graph network
        last_v = None
        for seg in gdf.itertuples():
            last_v = seg.v
        return last_v

    def get_first_u(self, gdf: geopandas) -> int: # uses graph functionality in the graph network
        for seg in gdf.itertuples():
            return seg.u

    def getincomingline(self, graphnetwork: geopandas, firstu) -> int: # uses graph functionality in the graph network
        idslist = list()
        for road in graphnetwork.itertuples():
            if road.v == firstu: # firstu of the current segment
                idslist.append(road.id)
        return idslist

    def getoutgoingline(self, graphnetwork: geopandas, lastv) -> int: # uses graph functionality in the graph network
        idslist = list()
        for road in graphnetwork.itertuples():
            if road.u == lastv: # lastv of the current segment
                idslist.append(road.id)
        return idslist