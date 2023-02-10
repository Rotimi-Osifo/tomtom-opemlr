import geopy
import geopy.distance as dist

def getfirstlementfromlist(itemslist: list) -> list:
    for listitem in itemslist:
        return list
    return None

def remove_duplicate_coordinates(coordinates: list) -> list:
    noduplicates: list = list()

    for point in coordinates:
        if noduplicates.count(point) == 0:
            noduplicates.append(point)

    return noduplicates


def get_distance_between_geodesic(first, second):
    return dist.geodesic(first, second).m


def get_index_of_item_from_list(path: list, item_id: int) -> int:
    idx:int = 0
    for roadid in path:

        if roadid == item_id:
            return idx

        idx = idx + 1

    return idx
