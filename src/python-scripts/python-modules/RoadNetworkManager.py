import GeometryData as gdata
import FeatureCollectionData as fcData
import neighbour_search as nb_s
import LinesCreator
import NodesCreator
import Nodes
import neighboursearch


class RoadNetworkManager:
    def __init__(self):
        self.mapAsfeaturesCollection = None
    
    def createlines(self, startId, targetNetwork, mainNetwork):
        geometryData = gdata.GeometryData()
        geometryData.setReferenceIds(targetNetwork)
        nb = nb_s.findNeighBoursFromNetwork(geometryData, targetNetwork, mainNetwork)

        ref_size = len(nb) + 1 
        geometryData.setReferenceSize(ref_size)
        nb_s.extractOrderedSequenceOfRoads(startId, nb, geometryData)

        linesCreator = LinesCreator.LinesCreator()
        lines = linesCreator.createLines(geometryData.targetIds, geometryData, targetNetwork)

        featureCollectionData = fcData.FeatureCollectionData()
        featureCollectionData.createCollectionsFromLines(lines.lines)

        self.mapAsfeaturesCollection = featureCollectionData.all_collection

#  nb_s.extractOrderedSequenceOfRoads(startId, nb, geometryData)

    def createlinesFromNetwork(self, targetNetwork, mainNetwork):
        geometryData = gdata.GeometryData()
        idList = list()
        startIdList = [4040302]
        neighbours_container = dict()
        cumDistanceList = 0

        nb = nb_s.findCloseNeighBoursFromNetworkExt(geometryData, \
                                                    targetNetwork, \
                                                    mainNetwork, \
                                                    startIdList, \
                                                    idList, \
                                                    neighbours_container, \
                                                    cumDistanceList)

        print(nb)

        linescreator = LinesCreator.LinesCreator()
        lines = linescreator.createLines( idList, geometryData, targetNetwork)

        featurecollectiondata = fcData.FeatureCollectionData()
        featurecollectiondata.createCollectionsFromLines(lines.lines)

        self.mapAsfeaturesCollection = featurecollectiondata.all_collection

    def createNodesFromGraphNetwork(self, targetNetwork, mainNetwork, graphroadnetwork):
        geometryData = gdata.GeometryData()
        idList = list()
        startIdList = [4040302]
        neighbours_container = dict()
        cumDistance = 0

        nb = nb_s.findCloseNeighBoursFromNetworkExt(geometryData, \
                                                    targetNetwork, \
                                                    mainNetwork, \
                                                    startIdList, \
                                                    idList, \
                                                    neighbours_container, \
                                                    cumDistance)
        nodesCreator = NodesCreator.NodesCreator()
        nodesCreator.createnodesfromgraph(graphroadnetwork, idList)


    def createNodesFromGraphNetworkExt(self, filtered_graph_nodes, filtered_network_graph):
        nsearch = neighboursearch.neighboursearch()
        idList = nsearch.findCloseNeighBoursFromNetwork(filtered_graph_nodes, filtered_network_graph)

        nodesCreator = NodesCreator.NodesCreator()
        nodesCreator.createnodesfromgraph(filtered_network_graph,  idList)

    def createlinesFromGraphNetwork(self, targetNetwork, mainNetwork, graphroadnetwork,  startIdList):
        geometryData = gdata.GeometryData()
        idList = list()
        neighbours_container = dict()
        cumDistance = 0

        nb = nb_s.findCloseNeighBoursFromNetworkExt(geometryData, \
                                                    targetNetwork, \
                                                    mainNetwork, \
                                                    startIdList, \
                                                    idList, \
                                                    neighbours_container, \
                                                    cumDistance)

        nodesCreator = NodesCreator.NodesCreator()
        nodes: Nodes = nodesCreator.createnodesfromgraph(graphroadnetwork, idList)

        linescreator = LinesCreator.LinesCreator()
        lines = linescreator.createConnectedRoadSegmentsFromGraph(graphroadnetwork, nodes.nodes)

        featurecollectiondata = fcData.FeatureCollectionData()
        featurecollectiondata.createCollectionsFromGraphLines(lines.lines, nodes.nodes)

        self.mapAsfeaturesCollection = featurecollectiondata.all_collection

    def createlinesFromGraphNetworkExt(self, filtered_graph_nodes, filtered_network_graph):
        connectedsegments = list()
        node_row = filtered_graph_nodes .iloc[0]
        u = node_row.id
        nsearch = neighboursearch.neighboursearch()
        #findCloseNeighBoursFromNetwork(self, nodes_gdf, edges, connectedsegments , u)
       #idList = nsearch.findCloseNeighBoursFromNetwork(filtered_graph_nodes, filtered_network_graph, connectedsegments, u)
        #idList = nsearch.findCloseNeighBoursFromNetwork(filtered_graph_nodes, filtered_network_graph)
        idList = nsearch.findCloseNeighBoursFromNetworkExt(filtered_network_graph)

        nodesCreator = NodesCreator.NodesCreator()
        nodes: Nodes = nodesCreator.createnodesfromgraph(filtered_network_graph, idList)

        linescreator = LinesCreator.LinesCreator()
        lines = linescreator.createConnectedRoadSegmentsFromGraph(filtered_network_graph, nodes.nodes)

        lines.printlines()

        featurecollectiondata = fcData.FeatureCollectionData()
        featurecollectiondata.createCollectionsFromGraphLines(lines.lines, nodes.nodes)

        self.mapAsfeaturesCollection = featurecollectiondata.all_collection
