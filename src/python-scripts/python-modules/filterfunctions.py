import constant_data as cData
class filterfunctions:

    def filternodes(self, nodes, filtered_network_graph):
        return (nodes[(nodes['id'].isin(filtered_network_graph.v)) | \
                      (nodes['id'].isin(filtered_network_graph.u))])

    def filterRoadNetwork(self, rNetwork):
        return (rNetwork[(rNetwork['name'].isin(cData.selected_road_names)) | \
                         (rNetwork['ref'].isin(cData.road_ref_list)) | \
                         (rNetwork['id'].isin(cData.road_id_list)) | \
                         (rNetwork['highway'].isin(["motorway_link", "trunk_link", "trunk"]))]
        )