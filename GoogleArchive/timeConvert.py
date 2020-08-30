"""Functions and classes for dealing with times."""
from __future__ import annotations  # Allows us to use HistoryElement type

import datetime
from typing import Sequence

def getHours(data: Sequence[HistoryElement]) -> Sequence[int]:
    """Get hours for the given data.

    Args:
        data (Sequence[HistoryElement]): elements to get the hours of.

    Returns:
        Sequence of ints for the hours (1-24) that correspond elementwise to the
        elements in data.
    
    Raises:
        ValueError: if any HistoryElement doesn't contain a TimeStamp
    """
    _checkData(data)
    return [x.timeStamp.hour for x in data]

# TODO - rename this to getWeekDays()
def getWeeks(data: Sequence[HistoryElement]) -> Sequence[int]:
    """Get the weeks for the given HistoryElements.

    Args:
        data (Sequence[HistoryElements]): elements to get weeks of

    Returns:
        Sequence of ints which correspond to the elements of data which are the
        weekdays of each element. Days are 0-6, where 0 is Monday and 6 is Sunday

    Raises:
        ValueError: if any HistoryElement doesn't contain a TimeStamp
    """
    _checkData(data)
    return [x.timeStamp.toDateTime().weekday() for x in data]

def _checkData(data: Sequence[HistoryElement]):
    """Check the given data to ensure the types and values are valid.

    Raises the proper exception if any data is invalid. Used for checking values
    for use in getting TimeStamp elements.

    Args:
        data (Sequence[HistoryElement]): The data to check

    Raises:
        ValueError: if any element doesn't contain a TimeStamp
    """
    if not all(x.timeStamp for x in data):
        raise ValueError("At least one element in data doesn't have a TimeStamp")

class TimeStamp:
    """Timestamp class used to convert time from original Strings in google files.

    Attributes:
        month (str): 3 letter representation of the month
        day (int): 1 based day of the month
        year (int): the year (e.g. 2020) 
        hour (int): hour, 0-23
        minute (int): minute, 0-59
        second (int): second, 0-59
    """

    def __init__(self, timeString: str):
        """Create a TimeStamp.

        Currently ignores the time zone.

        Args:
            timeString (str): String of the time as represented in Google documents.
                (e.g. 'Jan 11, 2015, 11:21:12 PM EDT')
        """
        #Example of input String and format
        #Jan 11, 2015, 11:21:12 PM EDT
        #"%b %-d, %Y, %-I:%M:%S %p %Z"
        dateList = timeString.split(',')
        self._month = dateList[0][0:3]
        self._day = int(dateList[0][-2:])
        self._year = int(dateList[1])

        dateList = dateList[2].split(':')
        self._minute = int(dateList[1])
        self._second = int(dateList[2][0:2])
        meridiem = dateList[2][3:5]
        self._hour = TimeStamp._adjustHour(int(dateList[0]), meridiem)

    @staticmethod
    def _adjustHour(hour: int, meridiem: str) -> int:
        """Adjust hour to be on 24 hour scale.

        Args:
            hour (int): hour, based on meridien time.

        Returns:
            The adjusted hour
        """
        if(meridiem == "PM" and hour < 12):
            hour += 12
        elif(meridiem == "AM" and hour == 12):
            hour = 0
        return hour

    @property
    def hour(self) -> int:
        """Hour of the TimeStamp."""
        return self._hour

    @property
    def month(self) -> str:
        """Month of the TimeStamp."""
        return self._month

    @property
    def day(self) -> int:
        """Day of the TimeStamp."""
        return self._day

    @property
    def year(self) -> int:
        """Year of the TimeStamp."""
        return self._year

    @property
    def minute(self) -> int:
        """Minute of the TimeStamp."""
        return self._minute

    @property
    def second(self) -> int:
        """Second of the TimeStamp."""
        return self._second

    @property
    def hour(self) -> int:
        """Hour of the TimeStamp."""
        return self._hour

    def toDateTime(self, interval: Optional[str] = 'day') -> datetime.datetime:
        """Convert a TimeStamp to a datetime.

        Returns:
            A datetime object with the same year, month, day attributes as the
            current TimeStamp (potentially modified based on interval)

        Raises:
            TypeError: if interval is not a string
            ValueError: if interval is not 'month', 'day', or 'year'
        """
        if not isinstance(interval, str):
            raise TypeError("interval must be of type str")
        if interval not in {'day', 'month', 'year'}:
            raise ValueError("interval must be one of 'month', 'day', or 'year'")
        months = {'Jan': 1,
                  'Feb': 2,
                  'Mar': 3,
                  'Apr': 4,
                  'May': 5,
                  'Jun': 6,
                  'Jul': 7,
                  'Aug': 8,
                  'Sep': 9,
                  'Oct': 10,
                  'Nov': 11,
                  'Dec': 12
                  }
        if interval == 'day':
            return datetime.datetime(self.year, months[self.month], self.day)
        elif interval == 'month':
            return datetime.datetime(self.year, months[self.month], 1)
        elif interval == 'year':
            return datetime.datetime(self.year, 1, 1)