"""Contains Functions for Parsing Google Files.

Functions:
    YoutubeSearchHistory
    YoutubeWatchHistory
    GoogleSearchHistory
"""
import os
from typing import Sequence

from . import timeConvert #Used to convert times found in files to TimeStamp objects
from ._htmlParse import Tag, loadHTML
from .historyElements import HistoryElement, SearchHistoryElement, WatchHistoryElement 

def YoutubeSearchHistory(takeoutPath: str) -> Sequence[SearchHistoryElement]:
    """Get Youtube Search History.

    Args:
        takeoutPath (str): path to your takeout folder (e.g.
            my/relative/path/to/Takeout/)
    
    Returns:
        Sequence of SearchHistoryElements for each one of your searches in
        your YoutubeSearchHistory

    Raises:
        FileNotFoundError: if the youtube search history file cannot be found.
            This is either because the specified path to takeout is wrong, the
            youtube search history wasn't included in your download, or Google
            changed the name of a folder/file since I last updated this
    """
    youtubeSearchPath = 'YouTube and Youtube Music/history/search-history.html'
    return _getSearchHistoryElements(takeoutPath, youtubeSearchPath)

def YoutubeWatchHistory(takeoutPath: str) -> Sequence[WatchHistoryElement]:
    """Get Youtube Watch History.

    Args:
        takeoutPath (str): path to your takeout folder (e.g.
            my/relative/path/to/Takeout/)
    
    Returns:
        Sequence of WatchHistoryElements for each one of your videos in your
        Youtube Watch History

    Raises:
        FileNotFoundError: if the youtube watch history file cannot be found.
            This is either because the specified path to takeout is wrong, the
            youtube watch history wasn't included in your download, or Google
            changed the name of a folder/file since I last updated this
    """
    youtubeWatchPath = 'YouTube and Youtube Music/history/watch-history.html'
    elements = _getElementsFromFile(takeoutPath, youtubeWatchPath)
    return [WatchHistoryElement(x) for x in elements]

def GoogleSearchHistory(takeoutPath: str) -> Sequence[SearchHistoryElement]:
    """Get Google Search History.

    Args:
        takeoutPath (str): path to your takeout folder (e.g.
            my/relative/path/to/Takeout/)
    
    Returns:
        Sequence of SearchHistoryElement for each one of your searches in your
        Google Search History

    Raises:
        FileNotFoundError: if the Google Search History file cannot be found.
            This is either because the specified path to takeout is wrong, serach
            history wasn't included in your download, or Google changed the name
            of a folder/file since I last updated this
    """
    googleSearchPath = 'My Activity/Search/MyActivity.html'
    return _getSearchHistoryElements(takeoutPath, googleSearchPath)

def _getSearchHistoryElements(takeoutPath: str, filePath: str) -> Sequence[SearchHistoryElement]:
    """Get Search History Elements.

    Intended to handle either Google or Youtube Search history.

    Args:
        takeoutPath (str): the path to the Takeout folder. Should end with
            'Takeout/' (e.g. 'some/path/to/Takeout/')
        filePath (str): the path to the file from within Takeout. Should end
            with the file, which must be a ".html" file

    Returns:
        Sequence of SearchHistoryElement for the given file containing the
        search history.

    Raises:
        ValueError: if the file is not an html file
        FileNotFoundError: if the given paths do not lead to a valid file
    """
    elements = _getElementsFromFile(takeoutPath, filePath)
    return [SearchHistoryElement(x) for x in elements]

def _getElementsFromFile(takeoutPath: str, filePath: str) -> Sequence[Tag]:
    """Get the head element of an HTML document at the given path.

    Args:
        takeoutPath (str): the path to the Takeout folder. Should end with
            'Takeout/' (e.g. 'some/path/to/Takeout/')
        filePath (str): the path to the file from within Takeout. Should end
            with the file, which must be a ".html" file
    
    Returns:
        Sequence of tags which are all elements that can be turned into
        HistoryElement objects

    Raises:
        ValueError: if the file is not an html file
        FileNotFoundError: if the given paths do not lead to a valid file
    """
    head = _getHeadElementFromFile(takeoutPath, filePath)
    return HistoryElement.getElementDivClass(head)

def _getHeadElementFromFile(takeoutPath: str, filePath: str) -> Tag:
    """Get the head element of an HTML document at the given path.

    Args:
        takeoutPath (str): the path to the Takeout folder. Should end with
            'Takeout/' (e.g. 'some/path/to/Takeout/')
        filePath (str): the path to the file from within Takeout. Should end
            with the file, which must be a ".html" file
    
    Returns:
        head tag of the given html file

    Raises:
        ValueError: if the file is not an html file
        FileNotFoundError: if the given paths do not lead to a valid file
    """
    if filePath.split(".")[-1] != "html":
        raise ValueError("The given filePath must lead to an HTML file")
    path = takeoutPath + filePath
    if not os.path.exists(path):
        raise FileNotFoundError("The path {} does not exist".format(path))
    return loadHTML(path)