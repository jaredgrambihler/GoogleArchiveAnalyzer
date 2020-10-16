"""Writes all URLs for Google Photos to a file."""
import os
import pathlib
import json

def photoURL(takeoutPath: str, outputFolder: str) -> None:
    """Output data on photo URLS, if present.

    Creates an output file, Photo_URLs.txt.
    File contains URLs of all photos on Google Photos.
    Prints out failure to find folder and number of file and folder errors encounters.

    Args:
        takeoutPath (str): relative path to takeout folder
        outputFolder (str): the name of the folder to output the data to in the
            current working directory.
    """
    # Will ignore any folders/files that have an error. Prints out the
    # number of errors upon termination.
    takeoutPath = pathlib.Path(takeoutPath)
    urlErrors = 0
    photosFolder = pathlib.Path(os.getcwd()).joinpath(takeoutPath).joinpath("Google Photos")
    if not photosFolder.exists():
        print("Photos folder does not exist. Skipping photos output.")
    if not photosFolder.is_dir():
        print("Photos folder is not a directory. Skipping photos output.")
    outputPath = pathlib.Path(os.getcwd()).joinpath(outputFolder.replace("\\", "")).joinpath('Photo_URLs.txt')
    with outputPath.open('w') as f:
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