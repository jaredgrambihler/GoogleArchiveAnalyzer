"""Analyze your Google Data.

This can be done through the analyzeData function that is present in this
module.
"""
import os
import time
from pathlib import Path
from typing import Sequence, Callable, Union

from . import parse, graph, photos, searchTerms
from .historyElements import HistoryElement

outputDir = Path.cwd().joinpath('GoogleArchiveData')
if outputDir.exists():
    print('Data directory already exists. Updated data will be written to {}'.format(outputDir))
else:
    try:
        outputDir.mkdir()
        print('Created Directory. Data will be wrriten to {}'.format(outputDir))
    except:
        raise Exception('Error in creating folder.')

def analyzeData(takeoutPath: Union[str, Path]):
    """Do analysis of all data.

    Runs analysis of PhotoURL, Purchase Data
    Youtube Search and Watch, and Google Search.

    Data is output via .png and .txt files to the GoogleArchiveData directory

    Args:
        takeoutPath (Union[str, Path]): Relative or absolute path to takeout folder.
            Can be either a string or a Path.
    
    Raises:
        FileNotFoundError: if the given path to takeout doesn't exist
        ValueError: if taekoutPath is not a folder
    """
    if isinstance(takeoutPath, str):
        takeoutPath = Path(takeoutPath)
    if not takeoutPath.exists():
        raise FileNotFoundError("The takeout path {} does not exist".format(takeoutPath))
    if not takeoutPath.is_dir():
        raise ValueError("The takeoutPath {} must be a folder".format(takeoutPath))

    photos.photoURL(takeoutPath, outputDir)
    # TODO - can't fix purchase data right now b/c I have none
    # purchase.getData(takeoutPath)
    
    YoutubeSearchData = parseData(parse.YoutubeSearchHistory,
                                   takeoutPath,
                                   "Youtube Search History")
    YoutubeWatchData = parseData(parse.YoutubeWatchHistory,
                                  takeoutPath,
                                  "Youtube Watch History")
    GoogleSearchData = parseData(parse.GoogleSearchHistory,
                                  takeoutPath,
                                  "Google Search History")

    allData = []
    if (YoutubeSearchData):
        allData.extend(YoutubeSearchData)
        searchData = [x for x in YoutubeSearchData if x.action=="Searched for"]
        graph.displayDataPlots(searchData, dir = outputDir)
    if (YoutubeWatchData):
        allData.extend(YoutubeWatchData)
        graph.displayDataPlots(YoutubeWatchData, title="Youtube Watch Data", dir = outputDir)
    if (GoogleSearchData):
        allData.extend(GoogleSearchData)
        graph.displayDataPlots(GoogleSearchData, title = 'Google Search', dir = outputDir)
    if(len(allData) > 0):
        graph.displayDataPlots(allData, title = 'All Search and Watch', dir = outputDir)

    searchTerms.commonSearchTerms(allData, 25, outputDir)

def parseData(func: Callable[[Path], Sequence[HistoryElement]],
               takeoutPath: Path,
               dataName: str
               ) -> Sequence[HistoryElement]:
    """Run the given parse function.

    Outputs information about time and errors.

    Args:
        func: the target function to use for parsing
        takeoutPath (Path): the path the the takeout folder, pass through to the
            parse function
        dataName (str): the name of the data, used in messages, such as
            (e.g. "google search")

    Returns:
        Sequence of HistoryElements from parsing the object, or an empty list if
        there was an error in parsing (most likely that we couldn't find the file)
    """
    start = time.time()
    data = []
    try:
        data = func(takeoutPath)
    except FileNotFoundError:
        print("Could not find {} data".format(dataName))
    except Exception as e:
        print("An unexcepted exception, {}, occured in parsing {}".format(e, dataName))
    finally:
        print("Took {}s to parse {}".format(time.time() - start, dataName))
    return data


#TODO - 
#parse chrome data
#parse maps
#parse location history
#number contacts
#mail