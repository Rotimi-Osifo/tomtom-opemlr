import pandas as pd

def road_class_to_kmph(road_class):
    """
    Returns a speed limit value based on road class,
    using typical Finnish speed limit values within urban regions.
    """
    if road_class == "motorway":
        return 100
    elif road_class == "motorway_link":
        return 80
    elif road_class in ["trunk", "trunk_link"]:
        return 60
    elif road_class == "service":
        return 30
    elif road_class == "living_street":
        return 20
    else:
        return 50

def fixNAForMaxSpeed(rNetwork):
    rNetwork["maxspeed"] = rNetwork["maxspeed"].astype(float).astype(pd.Int64Dtype())

    return rNetwork

def replaceNAInMaxSpeed(rNetwork):
    # Separate rows with / without speed limit information
    mask = rNetwork["maxspeed"].isnull()
    filtered_without_maxspeed = rNetwork.loc[mask].copy()
    filtered_with_maxspeed = rNetwork.loc[~mask].copy()

    # Apply the function and update the maxspeed
    filtered_without_maxspeed["maxspeed"] = filtered_without_maxspeed["highway"].apply(road_class_to_kmph)
    filtered_without_maxspeed.head(5).loc[:, ["maxspeed", "highway"]]

    filtered_network = filtered_with_maxspeed.append(filtered_without_maxspeed)
    filtered_network["maxspeed"] = filtered_network["maxspeed"].astype(int)

    return filtered_network
