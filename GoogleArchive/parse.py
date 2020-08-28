"""Contains Functions for Parsing Google Files

Functions:
    YoutubeSearchHistory
    YoutubeWatchHistory
    GoogleSearchHistory
"""
from typing import Sequence

from . import timeConvert #Used to convert times found in files to TimeStamp objects
from ._htmlParse import Tag, loadHTML
from .historyElements import HistoryElement, SearchHistoryElement, WatchHistoryElement 

def YoutubeSearchHistory(takeoutPath: str) -> Sequence[SearchHistoryElement]:
    path = takeoutPath + '/YouTube and Youtube Music/history/search-history.html'
    elements = HistoryElement.getElementDivClass(loadHTML(path))
    return [SearchHistoryElement(x) for x in elements]

def YoutubeWatchHistory(takeoutPath: str) -> Sequence[WatchHistoryElement]:
    path = takeoutPath + '/YouTube and Youtube Music/history/watch-history.html'
    elements = HistoryElement.getElementDivClass(loadHTML(path))
    return [WatchHistoryElement(x) for x in elements]

def GoogleSearchHistory(takeoutPath: str) -> Sequence[SearchHistoryElement]:
    path = takeoutPath + '/My Activity/Search/MyActivity.html'
    elements = HistoryElement.getElementDivClass(loadHTML(path))
    return [SearchHistoryElement(x) for x in elements]
