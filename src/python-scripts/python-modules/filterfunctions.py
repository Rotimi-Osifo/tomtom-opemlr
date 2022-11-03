
class filterfunctions:

    def filternodes(self, nodes, filtered_network_graph):
        return (nodes[(nodes['id'].isin(filtered_network_graph.v)) | \
                      (nodes['id'].isin(filtered_network_graph.u))])