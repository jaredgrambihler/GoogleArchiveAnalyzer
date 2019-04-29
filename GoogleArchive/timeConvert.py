import matplotlib.pyplot as plt
import datetime

timeZones = {'PST' : -3, 'MT': -2, 'CT': -1, 'EST':0, 'UTC': 5}

def getHours(data):
    """
    takes in a list of data (dicts of search data) and the time zone, converts into appropriate 24 hour time format.
    Currently returns only hours.
    """
    times = []
    for search in data:
        if (search['TimeStamp'] != None):
            times.append(search['TimeStamp'].hour)
    return times

def getWeeks(data):
    weeks = []
    for item in data:
        if (item['TimeStamp'] != None):
            weeks.append(item['TimeStamp'].toDateTime().weekday())
    return weeks

class TimeStamp:

    def __init__(self, timeString, timeZone):
        #Jan 11, 2015, 11:21:12 PM EDT
        #"%b %-d, %Y, %-I:%M:%S %p %Z"
        self.timeZone = timeZone

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
        if(self.meridiem == "PM" and self.hour != 12):
            self.hour += 12
        elif(self.meridiem == "AM" and self.hour == 12):
            self.hour += 12
        self.hour += timeZones[self.timeZone]
        if (self.hour <= 0):
            self.hour += 24
        elif (self.hour > 24):
            self.hour -=24
        return self.hour

    def toDateTime(self, interval = 'day'):
        month = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
        if interval == 'day':
            return datetime.datetime(self.year, month[self.month], self.day)
        elif interval == 'month':
            return datetime.datetime(self.year, month[self.month], 1)
        elif interval == 'year':
            return datetime.datetime(self.year, 1, 1)