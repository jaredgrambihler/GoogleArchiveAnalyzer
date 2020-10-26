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

def analyzeSematicJson(contents: dict) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Analyze the Semantic Location History JSON files.

    Args:
        contents (dict): the contents of the json file
    Returns:
        Two dataframes. The first is for activities and the second is for
        place vists.
    """
    pass

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
