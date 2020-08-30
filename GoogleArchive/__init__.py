"""Analyze your Google Data.

This can be done through the analyzeData function that is present in this
module.
"""

import os
import time
from typing import Sequence, Callable

from . import parse, graph, purchase, photos, searchTerms
from .historyElements import HistoryElement

dir = '\GoogleArchiveData\\'
path = os.getcwd()
if os.path.exists(path + dir):
    print('Data directory already exists. Updated data will be written to ' + path + dir)
else:
    try:
        os.mkdir(path + dir)
        print('Created Directory. Data will be wrriten to ' + path + dir)
    except:
        print('Error in creating folder.')
        raise Exception

def analyzeData(takeoutPath: str):
    """Do analysis of all data.

    Runs analysis of PhotoURL, Purchase Data
    Youtube Search and Watch, and Google Search.

    Data is output via .png and .txt files to the GoogleArchiveData directory

    Args:
        takeoutPath (str): Relative or absolute path to takeout folder.
            Whether relative or absolute, it is important that this ends with a
            '/' (e.g. 'my/path/to/Takeout/)
    
    Raises:
        FileNotFoundError: if the given path to takeout doesn't exist
        ValueError: if taekoutPath is not a folder
    """
    if not os.path.exists(takeoutPath):
        raise FileNotFoundError("The takeout path {} does not exist".format(takeoutPath))
    if not os.path.isdir(takeoutPath):
        raise ValueError("The takeoutPath {} must be a folder".format(takeoutPath))

    # TODO - update photos and purchase to work on the same takeoutPath instead
    # of still being relative
    photos.photoURL(path, dir)
    purchase.getData(path, dir)

    YoutubeSearchData = _parseData(parse.YoutubeSearchHistory,
                                   takeoutPath,
                                   "Youtube Search History")
    YoutubeWatchData = _parseData(parse.YoutubeWatchHistory,
                                  takeoutPath,
                                  "Youtube Watch History")
    GoogleSearchData = _parseData(parse.GoogleSearchHistory,
                                  takeoutPath,
                                  "Google Search History")

    allData = []
    if (YoutubeSearchData):
        allData.extend(YoutubeSearchData)
        searchData = [x for x in YoutubeSearchData if x.action=="Searched for"]
        graph.displayDataPlots(searchData, dir = dir)
    if (YoutubeWatchData):
        allData.extend(YoutubeWatchData)
        graph.displayDataPlots(YoutubeWatchData, title="Youtube Watch Data", dir = dir)
    if (GoogleSearchData):
        allData.extend(GoogleSearchData)
        graph.displayDataPlots(GoogleSearchData, title = 'Google Search', dir = dir)
    if(len(allData) > 0):
        graph.displayDataPlots(allData, title = 'All Search and Watch', dir = dir)

    searchTerms.commonSearchTerms(allData, 25, path, dir)

def _parseData(func: Callable[[str], Sequence[HistoryElement]],
               takeoutPath: str,
               dataName: str
               ) -> Sequence[HistoryElement]:
    """Run the given parse function.

    Outputs information about time and errors.

    Args:
        func: the target function to use for parsing
        takeoutPath (str): the path the the takeout folder, pass through to the
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
    except:
        print("An unexcepted exception occured in parsing {}".format(dataName))
    finally:
        print("Took {}s to parse {}".format(time.time() - start, dataName))
    return data


#TODO - 
#parse chrome data
#parse maps
#parse location history
#number contacts
#mail