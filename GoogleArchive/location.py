"""Analyze Location History."""
import json
from pathlib import Path
import pandas as pd

def getLatLong(d):
    """Get latitude and longitude from dict."""
    latitude = d['latitudeE7'] / 10000000
    longitude = d['longitudeE7'] / 10000000
    return latitude, longitude

def locationHistoryToDataFrame(locations: dict) -> pd.DataFrame:
    """Convert location history to a DataFrame."""
    """
    Possible keys

    'accuracy',
    'altitude',
    'heading',
    'latitudeE7',
    'longitudeE7',
    'timestampMs',
    'velocity',
    'verticalAccuracy'

    (Probably) Guaranteed

    'accuracy'
    'latitudeE7'
    'longitudeE7'
    'timestampMs'
    """
    errors = 0
    times = []
    latitudes = []
    longitudes = []
    accuracies = []
    for location in locations:
        try:
            time = location['timestampMs']
            latitude, longitude = getLatLong(location)
            accuracy = location['accuracy']
        except KeyError:
            errors += 1
            continue
        times.append(time)
        latitudes.append(latitude)
        longitudes.append(longitude)
        accuracies.append(accuracy)
    if errors != 0:
        print("{} errors in finding keys for locations".format(errors))
    return pd.DataFrame({"Time": times,
                         "Accuracy": accuracies,
                         "Latitude": latitudes,
                         "Longitude":longitudes
                         })

def analyzeLocationHistory(locationPath: Path, outputFolder: Path) -> None:
    """Analyze Location History.json file.

    Args:
        locationPath (Path): Path to location history folder
        outputFolder (Path): Path to output data to

    Raises:
        KeyError if the given json file has unexpected key names.
    """
    locationFile = locationPath.joinpath("Location History.json")
    if not locationFile.exists():
        print("Could not find location history file.")
        return
    
    with locationFile.open("r") as f:
        contents = json.load(f)
    try:
        locations = contents['location']
    except KeyError:
        raise KeyError("Location History.json does not have 'location' key")
    df = locationHistoryToDataFrame(locations)

def getActivitySegment(timeLineEvent: dict) -> dict:
    """Convert timeline of activity segment to our own dict.

    Args:
        timeLineEvent (dict): the dictionary for the timeline event

    Returns:
        A new dict with desired fields

    Raises:
        KeyError: if a desired field isn't found
    """
    activitySegment = timeLineEvent["activitySegment"]
    startLocation = activitySegment["startLocation"]
    endLocation = activitySegment["endLocation"]
    startLatitude, startLongitude = getLatLong(startLocation)
    endLatitude, endLongitude = getLatLong(endLocation)
    startDeviceTag = startLocation['sourceInfo']['deviceTag']
    endDeviceTag = endLocation['sourceInfo']['deviceTag']
    startTime = activitySegment['duration']['startTimestampMs']
    endTime = activitySegment['duration']['endTimestampMs']
    distance = activitySegment['distance']
    activityType = activitySegment['activityType']
    confidence = activitySegment['confidence']
    return {"StartLatitude":startLatitude,
            "startLongitude":startLongitude,
            "endLatitude":endLatitude,
            "endLongitude":endLongitude,
            "startDeviceTag":startDeviceTag,
            "endDeviceTag":endDeviceTag,
            "startTime":startTime,
            "endTime":endTime,
            "distance":distance,
            "activityType":activityType,
            "confidence":confidence}

def getPlaceVisit(timelineEvent: dict) -> dict:
    """Convert timeline of place visit to our own dict.

    Args:
        timeLineEvent (dict): the dictionary for the place visit

    Returns:
        A new dict with desired fields

    Raises:
        KeyError: if a desired field isn't found
    """
    placeVisit = timeLineEvent['placeVisit']
    location = placeVisit['location']
    latitude, longitude = getLatLong(location)
    address = location['address']
    name = location['name']
    # semanticType = location['semanticType']
    locationConfidence = location['locationConfidence']
    startTime = placeVisit['duration']['startTimestampMs']
    endTime = placeVisit['duration']['endTimestampMs']
    return {"latitude":latitude,
            "longitude": longitude,
            "address": address,
            "name": name,
            "locationConfidence": locationConfidence,
            "startTime": startTime,
            "endTime": endTime}

def analyzeSematicJson(contents: dict) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Analyze the Semantic Location History JSON files.

    Args:
        contents (dict): the contents of the json file
    Returns:
        Two dataframes. The first is for activities and the second is for
        place vists.
    """
    timeline = contents['timelineObjects']
    errors = 0
    unknown = 0
    activitySegments = []
    placeVisits = []
    for timeLineEvent in timeline:
        if 'activitySegment' in timeLineEvent:
            try:
                activitySegments.append(getActivitySegment(timeLineEvent))
            except KeyError:
                errors += 1
        elif "placeVisit" in timeLineEvent:
            try:
                placeVists.append(getPlaceVisit(timeLineEvent))
            except KeyError:
                errors += 1
        else:
            unknown += 1
    if errors != 0:
        print("Encountered {} errors while parsing semantic location history".format(errors))
    if unknown != 0:
        print("Found {} unknown entires in semantic location history".format(unknown))
    return pd.DataFrame(activitySegments), pd.DataFrame(placeVists)

def analyzeSemanticLocationHistory(locationPath: Path, outputFolder: Path) -> None:
    """Analyze Semantic Location History folder.

    Args:
        locationPath (Path): Path to location history folder
        outputFolder (Path): Path to output data to
    """
    semanticFolder = locationPath.joinpath("Semantic Location History")
    if not semanticFolder.exists():
        print("Could not find Semantic Location History file.")
        return
    activityDfs = []
    placeVisitDfs = []
    for semanticFile in semanticFolder.rglob("[0-9]" * 4 + "*.json"):
        with semanticFile.open("r") as f:
            contents = json.load(f)
            activityDf, placeVistDf = analyzeSematicJson(contents)
    activityDf = pd.concat(activityDfs)
    placeVistDf = pd.concat(placeVisitDfs)
    # TODO - use dataframe to analyze

def locationHistory(takeoutPath: Path, outputFolder: Path) -> None:
    """Analyze location history.

    Args:
        takeoutPath (Path): path to takeout folder
        outputFolder (Path): path to folder to output data
    """
    locationPath = takeoutPath.joinpath("Location History")
    if not locationPath.is_dir():
        print("'Location History' folder Location History was not found.")
        return
    try:
        analyzeLocationHistory(locationPath, outputFolder)
    except KeyError:
        print("Location History.json was not formatted as expected. Not analyzing.")
    analyzeSemanticLocationHistory(locationPath, outputFolder)
