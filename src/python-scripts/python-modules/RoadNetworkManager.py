import GeometryData as gdata
import FeatureCollectionData as fcData
import neighbour_search as nb_s
import LinesCreator
import NodesCreator
import Nodes
import neighboursearch
import roadnetworkgraphsearch

import trajectorydata
import connectedsegments


class RoadNetworkManager:

    def __init__(self):
        self.mapAsfeaturesCollection = None
        self.featurecollectiondata = None
        self.nodes = None
        self.lines = None
        self.idlist = None

    def getstartdata(self):
        startdatalist = list()

        startdatalistloc = startdata.trajectorydata(4040302, 1, "one_way_4040302_map_graph")
        startdatalist.append(startdatalistloc)
        startdatalistloc = startdata.trajectorydata(284402024, 2, "one_way_39887921_map_graph")
        startdatalist.append(startdatalistloc)
        startdatalistloc = startdata.trajectorydata(237772646, 1, "one_way_237772646_map_graph")
        startdatalist.append(startdatalistloc)
        startdatalistloc = startdata.trajectorydata(117090882, 2, "one_way_117090882_map_graph")
        startdatalist.append(startdatalistloc)

        return startdatalist

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
        lines = linescreator.createLines(idList, geometryData, targetNetwork)

        featurecollectiondata = fcData.FeatureCollectionData()
        featurecollectiondata.createCollectionsFromLines(lines.lines)

        self.mapAsfeaturesCollection = featurecollectiondata.all_collection

    def createNodesFromGraphNetwork(self, targetNetwork, mainNetwork, graphroadnetwork):
        geometryData = gdata.GeometryData()
        idList = list()
        startIdList = [39887921]
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
        nodesCreator.createnodesfromgraph(filtered_network_graph, idList)

    def createlinesFromGraphNetwork(self, targetNetwork, mainNetwork, graphroadnetwork, startIdList):
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
        node_row = filtered_graph_nodes.iloc[0]
        u = node_row.id
        nsearch = neighboursearch.neighboursearch()

        idList = nsearch.findCloseNeighBoursFromNetworkExt(filtered_network_graph)

        nodesCreator = NodesCreator.NodesCreator()
        nodes: Nodes = nodesCreator.createnodesfromgraph(filtered_network_graph, idList)

        linescreator = LinesCreator.LinesCreator()
        lines = linescreator.createConnectedRoadSegmentsFromGraph(filtered_network_graph, nodes.nodes)

        lines.printlines()

        featurecollectiondata = fcData.FeatureCollectionData()
        featurecollectiondata.createCollectionsFromGraphLines(lines.lines, nodes.nodes)

        self.mapAsfeaturesCollection = featurecollectiondata.all_collection

    def createlinesFromRoadGraphNetwork(self, targetNetwork, mainNetwork, graphroadnetwork):
            geometryData = gdata.GeometryData()
            startdatalist = self.getstartdata()
            idList = list()
            featurecollectiondata = fcData.FeatureCollectionData()
            for startdata in startdatalist:
                startIdList = [startdata.roadid]
                nb_s.findCloseNeighBoursFromRoadNetwork(geometryData, \
                                                        targetNetwork, \
                                                        mainNetwork, \
                                                        startIdList, \
                                                        idList)

                nodesCreator = NodesCreator.NodesCreator()
                nodes: Nodes = nodesCreator.createnodesfromgraph(graphroadnetwork, idList)

                linescreator = LinesCreator.LinesCreator()
                lines = linescreator.createConnectedRoadSegmentsFromGraph(graphroadnetwork, nodes.nodes, startdata.lanedirection)

                featurecollectiondata.createCollectionsFromGraphLines(lines.lines, nodes.nodes)


            self.mapAsfeaturesCollection = featurecollectiondata.all_collection
            self.nodes = nodes.nodes
            self.lines = lines.lines
            self.featurecollectiondata = featurecollectiondata
            self.idlist = idList

            data_path = "../../../data/"
            featurecollectiondata.writeCollection(data_path + "one_way_E6_map_graph.geojson", featurecollectiondata.all_collection)
            featurecollectiondata.writeCollection(data_path + "one_way_E6_map_graph_json.json", featurecollectiondata.all_collection)

    def buidConnectedSegmentsFromGraph(self, graphroadnetwork):
        roadnetwork_graphsearch = roadnetworkgraphsearch.roadnetworkgraphsearch()
        roadnetwork_graphsearch.buildconnectedsegments(graphroadnetwork)

        connected_segments = connectedsegments.connectedsegments()
        re_initializedsegments = connected_segments.build_connected_segments(roadnetwork_graphsearch.datastore, roadnetwork_graphsearch.segments)

        for startdataloc in roadnetwork_graphsearch.startdatalist:
            visitedset: list = roadnetwork_graphsearch.datastore[startdataloc.roadid]

            featurecollectiondata = fcData.FeatureCollectionData()
            featurecollectiondata.createCollectionsFromConnectedSegments(visitedset,  re_initializedsegments)

            data_path = "../../../data/"
            featurecollectiondata.writeCollection(data_path + startdataloc.mapfilename + ".geojson", featurecollectiondata.all_collection)
            featurecollectiondata.writeCollection(data_path + startdataloc.mapfilename + ".json", featurecollectiondata.all_collection)

        return roadnetwork_graphsearch





