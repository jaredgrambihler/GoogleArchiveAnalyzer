"""Classes for elements of history.

Every class is an implementation of HistoryElement.

Classes:
    HistoryElement (abstract class)
    SearchHistoryElement
    WatchHistoryElement
"""
from abc import ABC
from typing import Sequence, Tuple

from . import timeConvert
from ._htmlParse import Tag

_ELEMENT_DIV_CLASS = 'outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp'
_TITLE_CLASS = 'mdl-typography--title'
_ACTION_CLASS =  'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1'

"""Holds information such as prodcut, location, etc."""
# TODO - add parsing for informatin class
_INFORMATION_CLASS = 'content-cell mdl-cell mdl-cell--12-col mdl-typography--caption'

class HistoryElement(ABC):
    """Abstract class for elements.

    Defines an element of history, seach as a search query or a video that was
    watched.

    Attributes:
        prodcut
        action
        timeStamp
    """

    def __init__(self, tag: Tag):
        """Create a HistoryElement.
        
        Args:
            tag (Tag): the head tag of the element.

        Raises:
            ValueError: if the given tag is not of the proper class. The desired
                class is the elementDivClass attribute of the class.
        """
        if tag.className != _ELEMENT_DIV_CLASS:
            raise ValueError("element is not of the class {}".format(_ELEMENT_DIV_CLASS))

        self._action = HistoryElement._getAction(tag)
        self._timeStamp = HistoryElement._getTimeStamp(tag)
        self._product = HistoryElement._getProduct(tag)

    @property
    def product(self) -> str:
        return self._product

    @property
    def action(self) -> str:
        return self._action

    @property
    def timeStamp(self) -> timeConvert.TimeStamp:
        return self._timeStamp
    
    def __getitem__(self, item: str):
        """Get an item.

        Can be either 'product', 'action', or 'timeStamp'

        Args:
            item (str): the item to get. Case insensitive
        
        Returns:
            the value of the item
        """
        itemToValue = {"product": self.product,
                       "action": self.action,
                       "timestamp": self.timeStamp
                      }
        if item.lower() in itemToValue:
            return itemToValue[item.lower()]
        else:
            raise KeyError("The item {} does not exist in the given element")

    @staticmethod
    def getElementDivClass(headTag: Tag) -> Sequence[Tag]:
        return headTag.getTagsByClass(_ELEMENT_DIV_CLASS)

    @staticmethod
    def _getProduct(tag: Tag) -> str:
        """Get a product name from a tag.

        Looks for the 'mdl-typography--title' class.
        Assumes we are at an element where only one of these tags exists.

        Args:
            tag (Tag): either the tag of the title or a parent tag of the title
        
        Returns:
            the title as a string

        Raises:
            ValueError: if the tag we give isn't of the title class or doesn't have
                a number of titleTags equal to 1. This may also occur if the title
                tag doesn't have any text.
        """
        text = ""
        if tag.className == _TITLE_CLASS:
            text = tag.text
        else:
            titleTags = tag.getTagsByClass(_TITLE_CLASS)
            if len(titleTags) == 1:
                text = titleTags[0].text
            else:
                raise ValueError("The given tag contained {} title tags, but it \
                                should have exactly one".format(len(titleTags)))
        if text != "":
            return text
        else:
            raise ValueError("The given tags title class doesn't have any text.")

    @staticmethod
    def _getTimeStamp(tag: Tag) -> timeConvert.TimeStamp:
        actionElement = HistoryElement._getActionElement(tag)
        timeStamp = timeConvert.TimeStamp(actionElement.children[-1].text)
        return timeStamp

    @staticmethod
    def _getAction(tag: Tag) -> str:
        actionElement = HistoryElement._getActionElement(tag)
        action = actionElement.text.split("\xa0")[0]
        return action

    @staticmethod
    def _getActionElement(tag: Tag) -> Tag:
        data = tag.getTagsByClass(_ACTION_CLASS)
        if len(data) == 1:
            return data[0]
        else:
            raise ValueError("The given tag has more than one element for the action.")


class ChromeElement(HistoryElement):
    """Defines an element from Chrome activity.

    Attributes:
        product
        action
        timeStamp
        name
        url
    """

    def __init__(self, tag: Tag):
        """Create a ChromeElement.

        Args:
            tag (Tag): the head tag of the element.

        Raises:
            ValueError: if the given tag is not of the porper class. The desired
                class is the elementDivClass attribute of the class
        """
        super().__init__(tag)
        self._name, self._url = ChromeElement._getNameAndURL(tag)

    @property
    def name(self) -> str:
        """Website name."""
        return self._name 
    
    @property
    def url(self) -> str:
        """Website URL."""
        return self._url
    
    def __getitem__(self, item):
        """Get an item.

        Can be either 'product', 'action', 'timeStamp', 'name' or 'url'

        Args:
            item (str): the item to get. Case insensitive
        
        Returns:
            the value of the item
        """
        item = item.lower()
        if item == 'name':
            return self.name
        elif item == 'url':
            return self.url
        else:
            return super().__getitem__(item)

    @staticmethod
    def _getNameAndURL(tag: Tag) -> Tuple[str, str]:
        """Get name and URL from a tag.

        Args:
            tag (Tag): the tag to get the name and URL from

        Returns:
            Tuple of name, url
        """
        data = HistoryElement._getActionElement(tag)
        linkTags = data.getTagsByName("a")
        if len(linkTags) == 1:
            linkTag = linkTags[0]
            name = linkTag.text
            url = Tag.getLink(linkTag)
        elif data.text == "Used Chrome":
            name, url = "", ""
        else:
            raise ValueError("The given tag does not have a single <a> tag")
        return name, url
        

class SearchHistoryElement(HistoryElement):
    """Defines an element from Search History on either Google or Youtube.

    Attributes:
        prodcut
        action
        timeStamp
        query
    """

    def __init__(self, tag: Tag):
        """Create a SearchHistoryElement.
        
        Args:
            tag (Tag): the head tag of the element.

        Raises:
            ValueError: if the given tag is not of the proper class. The desired
                class is the elementDivClass attribute of the class.
        """
        super().__init__(tag)
        self._query = SearchHistoryElement._getQuery(tag)

    @property
    def query(self) -> str:
        return self._query

    def __getitem__(self, item):
        """Get an item.

        Can be either 'product', 'action', 'timeStamp', or 'query'

        Args:
            item (str): the item to get. Case insensitive
        
        Returns:
            the value of the item
        """
        if item.lower() == 'query':
            return self.query
        else:
            return super().__getitem__(item)

    @staticmethod
    def _getQuery(tag: Tag) -> str:
        """Create query from the given element tag.

        Args:
            element (Tag): the tag of the element. Should be of the _ELEMENT_DIV_CLASS
                class

        Returns:
            the query as a string
        """
        data = HistoryElement._getActionElement(tag)
        searchLinks = data.getTagsByName("a")

        if len(searchLinks) == 1:
            query = searchLinks[0].text
        elif len(searchLinks) == 0:
            query = data.text.split("\xa0")[1]
        else:
            raise ValueError("element given does not have appropriate length for links")
        return query

class WatchHistoryElement(HistoryElement):
    """Element for watch history from Youtube.

    Attributes:
        prodcut
        action
        timeStamp
        VideoLink
        VideoName
        ChannelLink
        ChannelName
    """

    def __init__(self, tag: Tag):
        super().__init__(tag)
        tags = tag.getTagsByName('a')
        # TODO - check what info we can get if this tag lenght isn't 2
        if len(tags) == 2:
            self._videoLink = Tag.getLink(tags[0])
            self._videoName = tags[0].text
            self._channelLink = tags[1].text
            self._channelName = Tag.getLink(tags[1])
        else:
            self._videoLink = ""
            self._videoName = ""
            self._channelLink = ""
            self._channelName = ""

    @property
    def videoLink(self):
        return self._videoLink

    @property
    def videoName(self):
        return self._videoName
    
    @property
    def channelLink(self):
        return self._channelLink

    @property
    def channelName(self):
        return self._channelName
    
    def __getitem__(self, item):
        """Get an item.

        Can be either 'product', 'action', 'timeStamp', 'VideoLink', 'VideoName',
        'ChannelLink', or 'ChannelName'

        Args:
            item (str): the item to get. Case insensitive
        
        Returns:
            the value of the item
        """
        itemToValue = {"videolink": self.videoLink,
                       "videoname": self.videoName,
                       "channellink": self.channelLink,
                       "channelname": self.channelName
                      }
        if item.lower() in itemToValue:
            return itemToValue[item.lower()]
        else:
            return super().__getitem__(item)