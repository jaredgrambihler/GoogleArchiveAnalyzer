"""Writes all URLs for Google Photos to a file."""
import os
from pathlib import Path
import json

def photoURL(takeoutPath: Path, outputFolder: Path) -> None:
    """Output data on photo URLS, if present.

    Creates an output file, Photo_URLs.txt.
    File contains URLs of all photos on Google Photos.
    Prints out failure to find folder and number of file and folder errors encounters.

    Args:
        takeoutPath (Path): path to takeout folder
        outputFolder (Path): path to the folder to output the data to
    """
    # Will ignore any folders/files that have an error. Prints out the
    # number of errors upon termination.
    urlErrors = 0
    photosFolder = takeoutPath.joinpath("Google Photos")
    if not photosFolder.exists():
        print("Photos folder does not exist. Skipping photos output.")
    if not photosFolder.is_dir():
        print("Photos folder is not a directory. Skipping photos output.")
    with outputFolder.joinpath('Photo_URLs.txt').open('w') as f:
        for folder in photosFolder.glob("*"):
            for photoFile in folder.glob("*.json"):
                if photoFile.name == "metadata.json":
                    continue
                with photoFile.open('r') as photoF:
                    fileDict = json.loads(photoF.read())
                    try:
                        f.write(fileDict["url"] + '\n\n')
                    except KeyError:
                        urlErrors += 1

    if(urlErrors > 0):
        print("Google Photos URLs not found: {}".format(urlErrors))