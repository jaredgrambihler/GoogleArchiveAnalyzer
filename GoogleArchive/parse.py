"""
Contains All Functions for Parsing Google Files
Functions:
    YoutubeSearchHistory
    YoutubeWatchHistory
    GoogleSearchHistory
    parse (Helper function)
"""
# %%
from typing import Sequence

from . import timeConvert #Used to convert times found in files to TimeStamp objects
from ._htmlParse import Tag, loadHTML

# TODO - add ability to set time zone
"""Time zone to be used when adjusting time entries."""
_TIME_ZONE = 'PST'    

"""The Div class name for the elements. Each entry of search, watch, etc. is within this."""
_ELEMENT_DIV_CLASS = 'outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp'

"""Contains information about the action and what it was.

This could be seomthing such as search, watch, as well as the link, channel, etc.
"""
_ACTION_CLASS = 'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1'

"""Used for the title of an element, based on product name"""
_TITLE_CLASS = 'mdl-typography--title'

"""Holds information such as prodcut, location, etc."""
_INFORMATION_CLASS = 'content-cell mdl-cell mdl-cell--12-col mdl-typography--caption'

def YoutubeSearchHistory(takeoutPath):
    path = takeoutPath + '/YouTube and Youtube Music/history/search-history.html'
    elements = _getElementDivClass(loadHTML(path))
    data = []
    errors = 0
    for element in elements:
        try:
            data.append(_createSearchDataFromElement(element))
        except ValueError:
            errors += 1
    print("Encountered {} errors in parsing Youtube Search History".format(errors))
    return data

def YoutubeWatchHistory(takeoutPath):
    path = takeoutPath + '/YouTube and Youtube Music/history/watch-history.html'
    elements = [tag for tag in loadHTML(path) if tag.className == _ACTION_CLASS]
    data = []
    for element in elements:
        elementDict = {'Product': 'Youtube',
                       'Action': 'Watch',
                       'TimeStamp': None,
                       'VideoLink': None,
                       'VideoName': None,
                       'ChannelLink': None,
                       'ChannelName': None
                       }
        tags = element.children
        elementDict["TimeStamp"] = timeConvert.TimeStamp(tags[-1].text, _TIME_ZONE)
        # We only need the other tags for timestamp
        # If we have both the video link and the channel, there are two a tags.
        # If the video is private or removed, we will have one or zero tags
        tags = [tag for tag in tags if tag.name == 'a']
        if len(tags) == 2:
            elementDict["VideoName"] = tags[0].text
            elementDict["VideoLink"] = Tag.getLink(tags[0])
            elementDict["ChannelName"] = tags[1].text
            elementDict["ChannelLink"] = Tag.getLink(tags[1])
        data.append(elementDict)
    return data

def GoogleSearchHistory(takeoutPath):
    path = takeoutPath + '/My Activity/Search/MyActivity.html'
    elements = _getElementDivClass(loadHTML(path))
    data = []
    errors = 0
    for x in elements:
        try:
            data.append(_createSearchDataFromElement(x))
        except ValueError:
            errors += 1
    print("{} errors in parsing Google Search History".format(errors))
    return data

def _getElementDivClass(headTag: Tag) -> Sequence[Tag]:
    return headTag.getTagsByClass(_ELEMENT_DIV_CLASS)

def _createSearchDataFromElement(element: Tag) -> dict:
    """Create search data dict from the given element tag.

    Args:
        element (Tag): the tag of the element. Should be of the _ELEMENT_DIV_CLASS
            class

    Returns:
        dict for the given element

    Raises:
        ValueError: if the given element is not of _ELEMENT_DIV_CLASS, or if there
            is more than one element for the given action
    """
    if element.className != _ELEMENT_DIV_CLASS:
        raise ValueError("element is not of the class {}".format(_ELEMENT_DIV_CLASS))
    data = element.getTagsByClass(_ACTION_CLASS)
    if len(data) == 1:
        data = data[0]
    else:
        raise ValueError("The given tag has more than one element for the action.")
    timeStamp = timeConvert.TimeStamp(data.children[-1].text, _TIME_ZONE)
    action = data.text.split("\xa0")[0]
    searchLinks = data.getTagsByName("a")

    if len(searchLinks) == 1:
        query = searchLinks[0].text
    elif len(searchLinks) == 0:
        query = data.text.split("\xa0")[1]
    else:
        raise ValueError("element given does not have appropriate length for links")

    product = _getProductFromTag(element)

    return {
            'Product': product, 
            'Action': action, 
            'Query': query,
            'TimeStamp' : timeStamp
            }

def _getProductFromTag(tag: Tag) -> str:
    """Get a product name from a tag.

    Looks for the 'mdl-typography--title' class.
    Assumes we are at an element where only one of these tags exists.

    Args:
        tag (Tag): either the tag of the title or a parent tag of the title
    
    Returns:
        the title as a string

    Raises:
        ValueError: if the tag we give isn't of the title class and doesn't have
            a number of titleTags equal to 1.
    """
    # TODO - check that text isn't empy
    if tag.className == _TITLE_CLASS:
        return tag.text
    else:
        titleTags = tag.getTagsByClass(_TITLE_CLASS)
        if len(titleTags) == 1:
            return titleTags[0].text
        else:
            raise ValueError("The given tag contained {} title tags, but it \
                              should have exactly one".format(len(titleTags)))