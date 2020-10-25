"""Analyze Location History."""
import json
from pathlib import Path

def analyzeLocationHistory(locationPath: Path, outputFolder: Path) -> None:
    """Analyze Location History.json file.

    Args:
        locationPath (Path): Path to location history folder
        outputFolder (Path): Path to output data to
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
    # TODO - actually analyze it

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
    analyzeLocationHistory(locationPath, outputFolder)
    analyzeSemanticLocationHistory(locationPath, outputFolder)
