class neighboursearch:

    def __get_gdf_from_u(self, u_gdf, edgesnetwork):
        for edge in u_gdf.itertuples():
            return edgesnetwork[edgesnetwork['id'] == edge.id]

    def __get_road_id_from_single_gdf(self, gdf):
        for seg in gdf.itertuples():
            return seg.id

    def __get_last_v(self, gdf):
        last_v = None
        for seg in gdf.itertuples():
            last_v = seg.v
        return last_v

    def findCloseNeighBoursFromNetwork(self, nodes_gdf, edges):
        connectedsegments = list()
        for node in nodes_gdf.itertuples():
            u = node.id
            single_node_gdf = edges[edges['u'] == u]
            road_segment_gdf = self.__get_gdf_from_u(single_node_gdf, edges)
            if road_segment_gdf is not None:
                road_id = self.__get_road_id_from_single_gdf(road_segment_gdf)
                if road_id is not None:
                    if connectedsegments.count(road_id) == 0:
                        connectedsegments.append(road_id)
                u = self.__get_last_v(road_segment_gdf)
        return connectedsegments