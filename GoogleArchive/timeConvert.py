import datetime #Needed to convert TimeStamp object to datetime object

timeZones = {'PST' : -3, 'MT': -2, 'CT': -1, 'EST':0, 'UTC': 5} #Used to convert time zones, base is EST

def getHours(data):
    """
    Returns a list of hours for a given list of data.
    Args:
        Data: List of dictionaries. Dictionaries need 'TimeStamp' as a key to a TimeStamp object.
    """
    times = []
    for search in data:
        if (search['TimeStamp'] != None):
            times.append(search['TimeStamp'].hour)
    return times

def getWeeks(data):
    """
    Returns a list of weekdays as defined by datetime. 
    Each entry is an int where Monday is 0, Sunday is 6.
    Args:
        Data: List of dictionaries. Dictionaries need 'TimeStamp' as a key to a TimeStamp object.
    """
    weeks = []
    for item in data:
        if (item['TimeStamp'] != None):
            weeks.append(item['TimeStamp'].toDateTime().weekday())
    return weeks

class TimeStamp:
    """Timestamp class used to convert time from original Strings in google files.

    Data:
         month
         day
         year
         timeZone
         hour
         minute
         second
    """

    # TODO - the time zone should come from the time stamp
    def __init__(self, timeString):
        """
        Sole constructor for the class.
        Creates object and sets time zone to be correct.

        Args:
            timeString: String of the time as represented in Google documents.
        """
        #Example of input String and format
        #Jan 11, 2015, 11:21:12 PM EDT
        #"%b %-d, %Y, %-I:%M:%S %p %Z"
        # self.timeZone = timeZone

        dateList = timeString.split(',')
        self.month = dateList[0][0:3]
        self.day = int(dateList[0][-2:])
        self.year = int(dateList[1])

        dateList = dateList[2].split(':')
        self.hour = int(dateList[0])
        self.minute = int(dateList[1])
        self.second = int(dateList[2][0:2])
        self.meridiem = dateList[2][3:5]
        self.adjustTimeZone()

    def adjustTimeZone(self):
        """
        Adjusts time zone of data to specified time zone.
        Adjusts time to be on 24 hour scale based on meridiem.
        Returns the adjusted hour.
        """
        if(self.meridiem == "PM" and self.hour != 12):
            self.hour += 12
        elif(self.meridiem == "AM" and self.hour == 12):
            self.hour += 12
        # self.hour += timeZones[self.timeZone]
        if (self.hour <= 0):
            self.hour += 24
        elif (self.hour > 24):
            self.hour -=24
        return self.hour

    def toDateTime(self, interval = 'day'):
        """
        Returns a datetime object with the same year, month, day attributes as the current object.
        Args:
            interval (optional): 'day' by default. Can be 'month' or 'year'.
                Using 'month' set day field to 1, using 'year' sets day and month fields to 1
        """
        month = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
        if interval == 'day':
            return datetime.datetime(self.year, month[self.month], self.day)
        elif interval == 'month':
            return datetime.datetime(self.year, month[self.month], 1)
        elif interval == 'year':
            return datetime.datetime(self.year, 1, 1)