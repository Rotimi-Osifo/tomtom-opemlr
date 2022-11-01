import GeometryData as gdata
import FeatureCollectionData as fcData
import neighbour_search as nb_s
import LinesCreator

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

    def createlinesFromGraphNetwork(self, targetNetwork, mainNetwork, graphroadnetwork):
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

            print('nb -:', nb)

            linescreator = LinesCreator.LinesCreator()
            lines = linescreator. createConnectedRoadSegments(graphroadnetwork, idList)

            featurecollectiondata = fcData.FeatureCollectionData()
            featurecollectiondata.createCollectionsFromGraphLines(lines.lines)

            self.mapAsfeaturesCollection = featurecollectiondata.all_collection


