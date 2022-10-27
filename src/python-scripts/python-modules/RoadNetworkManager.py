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
        lines = linesCreator.createLines( geometryData.targetIds, geometryData, targetNetwork)

        featureCollectionData = fcData.FeatureCollectionData()
        featureCollectionData.createCollectionsFromLines(lines.lines)

        self.mapAsfeaturesCollection = featureCollectionData.all_collection


