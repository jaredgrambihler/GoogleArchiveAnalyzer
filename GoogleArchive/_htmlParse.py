"""Functions for parsing HTML."""
# %%
from __future__ import annotations  # We need this to use Tag type in Tag class
from pathlib import Path
import re
import os

from typing import Sequence, Optional

class Tag:
    """Defines an HTML tag.

    Attributes:
        name (str): the name of the tag (e.g. div, html)
        text (str): the text that the tag contains
        parent (Tag): the parent of the current tag
        children (Sequence[tag]): the children of the current tag
    """

    def __init__(self, tagString: str, parent: Tag, text: Optional[str] = "",
                 children = []) -> None:
        """Create a Tag.

        Args:
            tagString (str): the raw text of the tag, including brackets
            parent (Tag): the parent of the current tag
            children (Sequence[Tag]): tags for any children
        """
        self._tagString = tagString
        self._parent = parent
        self._text = text
        self._children = list(children)

    @staticmethod
    def _getNameFromTagString(tagString: str) -> str:
        return re.split("[> ]", tagString)[0][1:]

    @staticmethod
    def getLink(tag: Tag) -> str:
        """Get the link from a tag, if it exists.

        Args:
            tag (Tag): tag to get the link from

        Returns:
            string of the link, if it exists. If there is no link, returns
            the empty string

        Raises:
            ValueError: If the given tag is not an "a" tag
        """
        return tag._getTagProperty("href")

    def _getTagProperty(self, name: str) -> str:
        # TODO - this will stop at an escaped quote
        tagRegex = name + '="[^"]*"'
        names = re.findall(tagRegex, self._tagString)
        if names:
            # TODO - add some sort of check here that we don't find multiple matches
            value = "".join(names[0].split("=")[1:])
            # remove first and last quotes
            return value[1:-1]
        return ""

    @property
    def name(self) -> str:
        """The name of the tag."""
        return Tag._getNameFromTagString(self._tagString)

    @property
    def className(self) -> str:
        """The class of the tag, if it exists, otherwise the empty string."""
        return self._getTagProperty("class")    
    
    @property
    def text(self) -> str:
        """The text of the tag."""
        return self._text

    @property
    def parent(self) -> Tag:
        """Parent tag of the current tag.

        May be None if the current tag is the top tag of the document."""
        return self._parent
    
    @property
    def children(self) -> Sequence[Tag]:
        """The child Tags of the current Tag."""
        return tuple(self._children)
    
    def setText(self, text: str) -> None:
        """Set the text of the current tag."""
        self._text = text
    
    def addChild(self, tag: Tag):
        """Add a Tag as a child of the current Tag."""
        self._children.append(tag)

    def __repr__(self):
        """Represent self as name, text and the parent tags name."""
        parentDisplayName = self.parent.name if self.parent is not None else "None"
        return "Name: {}, Class: {}, Text: {}, Parent Tag: {}". \
                format(self.name, self.className, self.text, parentDisplayName)
    
    def __str__(self):
        """Represent self as name, text and the parent tags name."""
        return self.__repr__()

    def __iter__(self):
        """Iterate over Tags.

        Iterates over each child, and at each child we recursively iterate
        through that child before moving on to the next child.
        """
        for child in self.children:
            yield child
            # Recursively iterate through child
            for x in child:
                yield x

    def getTagsByName(self, tagName: str) -> Sequence[Tag]:
        """Gets tag by their tag name.

        Args:
            tagName (str): name of the tags to get

        Returns:
            Sequence of tags with the tag name that are within the current tag.
            The order is based on a depth first search through the tags.
        """
        tags = []
        for tag in self:
            if tag.name == tagName:
                tags.append(tag)
        return tags

    def getTagsByClass(self, className: str) -> Sequence[Tag]:
        """Get tags with the given className.

        Args:
            className (str): the className of tags to get
        
        Returns:
            Sequence of tags with that className that are within the current
            tag. The order is based on a depth first search through the tags.
        """
        tags = []
        for tag in self:
            if tag.className == className:
                tags.append(tag)
        return tags

def _generateTags(tags: Sequence[str], texts: Sequence[str]) -> None:
    """Generate the tag structure based on parsed tags and texts.

    Args:
        tags (Sequence[str]): The tags of the document. Sepcifically, these are
            both opening and closing tags, and they have not been stripped of 
            their open and closing brackets (e.g. a tag would be '<html>' not
            'html'). Any comment tag is ignored.
        texts (Sequence[str]): The texts of the document. The ith text corresponds
            to the ith tag. Closing tags should have an empty string associated
            with them, as there is nothing between the closing tag and the next
            opening tag.
    
    Returns:
        Tag which is the head tag of the document
    """
    headTag = Tag(tags[0], None, tuple())

    currentParent = headTag

    for tag, text in zip(tags[1:], texts[1:]):
        if currentParent == None:
            print("Ran out of parents at {}".format(text))
            break
        if tag[:3] == "<!--" or tag == "<br>":
            # comments or breaks have no closing tag
            currentParent.addChild(Tag(tag, currentParent, text))
        elif tag[:2] == "</":
            # Ending tag, move control up
            currentParent = currentParent.parent
        elif tag[:1] == "<":
            cur = Tag(tag, currentParent, text)
            currentParent.addChild(cur)
            currentParent = cur
        else:
            currentParent.setText(tag)

    return headTag

def generateTags(html: str) -> Tag:
    """Generate tags for an HTML string.

    Args:
        html (str): the string of the HTML
    
    Returns:
        Tag object which is the head tag of the HTML
    """
    tagRegex = re.compile("<[^>]*>")
    tags = re.findall(tagRegex, html)
    texts = re.split(tagRegex, html)
    texts = texts[1:]   # Ignore the first "" before open tag
    tags = [tag.strip() for tag in tags]
    texts = [text.strip() for text in texts]
    return _generateTags(tags, texts)

def loadHTML(path: Path) -> Tag:
    """Load HTML and return the head tag.

    Args:
        path (str): Path the the HTML file
    
    Returns:
        Tag which is the head tag of the HTML document

    Raises:
        ValueError: if the given path doesn't exist
    """
    if not path.is_file():
        raise ValueError("The given path {} does not exist or is not a file".format(path))
    with path.open('r', encoding="UTF-8") as f:
        htmlString = f.read()
    return generateTags(htmlString)

"""
# %%
import time
start = time.time()
path = "../Takeout/YouTube and Youtube Music/history/watch-history.html"
# This target class could be changed by Google
# Good place to check if this breaks in the future
targetTagClass = 'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1'
elements = [tag for tag in loadHTML(path) if tag.className == targetTagClass]
print("Took {}s to run".format(time.time()-start))

# %%
from collections import Counter
print(Counter(len(x.children) for x in elements))

for x in elements:
    if len(x.children) in {2, 1}:
        continue
"""