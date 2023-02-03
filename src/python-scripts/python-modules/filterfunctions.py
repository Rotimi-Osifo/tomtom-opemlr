import constant_data as cData
import geopandas


class filterfunctions:

    def filternodes(self, nodes: geopandas, filtered_network_graph: geopandas) -> geopandas:
        return (nodes[(nodes['id'].isin(filtered_network_graph.v)) | \
                      (nodes['id'].isin(filtered_network_graph.u))])

    def filterRoadNetwork(self, rNetwork: geopandas) -> geopandas:
        return (rNetwork[(rNetwork['name'].isin(cData.selected_road_names)) | \
                         (rNetwork['ref'].isin(cData.road_ref_list)) | \
                         (rNetwork['id'].isin(cData.road_id_list)) | \
                         (rNetwork['highway'].isin(["motorway_link", "trunk_link", "trunk"]))]
        )

    def filternetworkWithGraphAndNonGraph(self, graphNetwork: geopandas, nongraphrnetwork: geopandas) -> geopandas:
        return (nongraphrnetwork[(graphNetwork['name'].isin(cData.selected_road_names)) | \
                                 (graphNetwork['ref'].isin(cData.road_ref_list)) | \
                                 (graphNetwork['id'].isin(cData.road_id_list)) | \
                                 (graphNetwork['highway'].isin(["motorway_link", "trunk_link", "trunk"]))]
        )

    def filterRoadNetworkWithRef(self, rNetwork: geopandas, roadreflist: list) -> geopandas:
        return (rNetwork[(rNetwork['ref'].isin(roadreflist))]
        )

    def filterRoadNetworkWithRefAndName(self, rNetwork: geopandas, roadreflist: list) -> geopandas:
        return (rNetwork[(rNetwork['ref'].isin(roadreflist)) |
                         (rNetwork['name'].isin(roadreflist)) |
                         (rNetwork['id'].isin(cData.road_id_list))
        ]
        )

    def filterRoadNetworkWithRefAndNameExt(self, rNetwork: geopandas, road_id_list: list, roadreflist: list) -> geopandas:
        return (rNetwork[(rNetwork['ref'].isin(roadreflist)) |
                         (rNetwork['name'].isin(roadreflist)) |
                         (rNetwork['id'].isin(road_id_list))
                         ]
        )

    def filterRoadNetworkWithId(self, rNetwork: geopandas, roadidlist: list) -> geopandas:
        return (rNetwork[(rNetwork['id'].isin(roadidlist))]
        )

    #
    def filterRoadNetworkWithNegationAndCopy(self, rNetwork: geopandas) -> geopandas:
        return (rNetwork.loc[
                    ~rNetwork["highway"].isin(['cycleway', 'footway', 'pedestrian', 'trail', 'crossing'])].copy()
                )

    def filterRoadNetworkWithRefAndNames(self, rNetwork: geopandas, roadnames:list, roadrefs:list) -> geopandas:
        return (rNetwork[(rNetwork['name'].isin(roadnames)) | \
                         (rNetwork['ref'].isin(roadrefs))]
        )