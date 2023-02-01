
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