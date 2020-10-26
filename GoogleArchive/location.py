"""Analyze Location History."""
import json
from pathlib import Path

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
    with locationFile.open("r") as f:
        contents = json.load(f)
    try:
        locations = contents['location']
    except KeyError:
        raise KeyError("Location History.json does not have 'location' key")
    

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
    # TODO - actually analyze it

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
