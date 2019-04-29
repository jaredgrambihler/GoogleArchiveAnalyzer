#Contains All Functions for Parsing Google Files
import time
import GoogleArchive.common as common
import GoogleArchive.timeConvert as timeConvert
import GoogleArchive.graph as graph

timeZone = 'PST'

import time

def parse(dir, checkDict, checkList):
    try:
        with open(dir, 'r', encoding='utf-8') as f:
            text= f.read()
            f.close()
    except:
        print('Error: Cannot open file for ' + dir)
        return None

    def checkStr(str, checkDict):
        if('div class' in str):
            return False
        if ('p class' in str):
            return False
        for check in checkList:
            if(check in str):
                return False
        htmlStrings = {'', 'body', 'br', '/p', '/div', 'b', '/b', '/a', '/body', '/html', 'a href'}
        if str in htmlStrings:
            return False
        if str in checkDict:
            return False
        return True

    text = text.split('</head>')
    text = text[1].split('<')
    arr = []

    errorCount = -1 #-1 accounts for an empty string that will always result in one error as it cannot be split.
    for t in text:
        temp = t.split('>')
        try:
            if(checkStr(temp[0], checkDict)):
               arr.append(temp[0])
            if(checkStr(temp[1], checkDict)):
                arr.append(temp[1])
        except:
            errorCount += 1
    if errorCount != 0:
        print(errorCount, "error(s) occured in parsing of " + dir + '.')

    return arr

def DriveHistory():
    """
    Data Format
    {
    'Product' : 'Drive'
    'Action' : [Action List]
    'TimeStamp' : TimeStamp Object
    'Details': {'FromIP': 'IP'}
    }
    """
    checkDict = {'Drive', 'Products:', '&emsp;Drive', 'Details:'}
    checkList = []
    arr = parse('My Activity\Drive\MyActivity.html', checkDict, checkList)
    if arr == None:
        return None
    data = []
    for i in range(len(arr) // 4):
        currentPlace = i * 4
        data.append({'Product': 'Drive', 'Action': [], 'TimeStamp': None, 'Details': None})
        data[i]['Action'].append(arr[currentPlace])
        data[i]['Action'].append(arr[currentPlace + 1])
        data[i]['TimeStamp'] = timeConvert.TimeStamp(arr[currentPlace + 2], timeZone)
        data[i]['Details'] = arr[currentPlace + 3][6:] # [6:] removes escape characters
    return data

def YoutubeSearchHistory():
    """
    Data Format
    {
    'Product' : 'Youtube'
     'Action' : 'Search'
     'TimeStamp' : TimeStamp Object
     'Search' : 'Search Queury'
     }
    """
    checkDict = {'Searched for\xa0', 'www.youtube.com', 'Products:', '&emsp;YouTube', "YouTube"}
    checkList = ['a href="https://www.youtube.com/results?search_query=']
    arr = parse('YouTube/history/search-history.html', checkDict, checkList)
    if arr == None:
        return None
    data = []
    #Search, Date
    for i in range(len(arr)//2):
        arrPlace = 2 * i
        data.append( {'Product': 'Youtube', 'Action': 'Search', 'TimeStamp': None, 'Search': None} )
        data[i]['Search'] = arr[arrPlace]
        data[i]['TimeStamp'] = timeConvert.TimeStamp(arr[arrPlace + 1], timeZone)
    return data

def YoutubeWatchHistory():
    """
    Data Format:
    {
    'Product': 'Youtube',
    'Action': 'Watch',
    'TimeStamp': TimeStamp Object,
    'VideoLink': None,
    'VideoName': None,
    'ChannelLink': None,
    'ChannelName': None
    }
    """
    #FILE FORMAT: (3 Possible scenarios)
    #'Youtube', 'Watched\xa0', 'a href="VIDEO LINK"', 'VIDEO NAME', 'a href="CHANNEL LINK"', 'CHANNEL NAME', 'TIMESTAMP', 'Products:', '&emsp:Youtube'
    #'Youtube', 'Watched a video that has been removed', 'TIMESTAMP', 'Products:', '&emsp:Youtube'
    #'Youtube', 'Watched\xa0', 'a href="VIDEO LINK"', 'VIDEO LINK', 'TIMESTAMP', 'Products:', '&emsp:Youtube'

    checkDict = {'Products:', '&emsp;YouTube'} #eliminates the last 2 chunks of any given data sequence that may be found
    checkList = []
    arr = parse('YouTube\history\watch-history.html', checkDict, checkList)
    if arr == None:
        return None
    data = []
    #'Youtube', 'Watched\xa0', 'a href="VIDEO LINK"', 'VIDEO NAME', 'a href="CHANNEL LINK"', 'CHANNEL NAME', 'TIMESTAMP' - length of 7
    #'Youtube', 'Watched a video that has been removed', 'TIMESTAMP' - length of 3
    #'Youtube', 'Watched\xa0', 'a href="VIDEO LINK"', 'VIDEO LINK', 'TIMESTAMP' - length of 5
    for i in range(len(arr)):
        currentEntry = []
        if( arr[i] == 'YouTube'): #indicates start of a new entry
            data.append({'Product': 'Youtube', 'Action': 'Watch', 'TimeStamp': None, 'VideoLink': None, 'VideoName': None, 'ChannelLink': None, 'ChannelName': None})
            j = 1
            while ( i+j < len(arr) and arr[i+j] != 'YouTube'): #goes until next entry
                currentEntry.append(arr[i+j])
                j += 1
        if (len(currentEntry) == 6): #lengths here are shortened by 1 as 'Youtube' is not appended to the currentEntry 
            #'Youtube', 'Watched\xa0', 'a href="VIDEO LINK"', 'VIDEO NAME', 'a href="CHANNEL LINK"', 'CHANNEL NAME', 'TIMESTAMP'
            try:
                data[len(data)-1]['VideoLink'] = arr[i+2][7:-1] #eliminates "" and 'a href ='
                data[len(data)-1]['VideoName'] = arr[i+3]
                data[len(data)-1]['ChannelLink'] = arr[i+4]
                data[len(data)-1]['ChannelName'] = arr[i+5]
                data[len(data)-1]['TimeStamp'] = timeConvert.TimeStamp(arr[i+6], timeZone)
            except:
                print('Error in Youtube Watch Data for len(6). Error Data:', arr[i:i+8], '\n')
        elif(len(currentEntry) == 4):
            #'Youtube', 'Watched\xa0', 'a href="VIDEO LINK"', 'VIDEO LINK', 'TIMESTAMP'
            #'YouTube', 'Watched\xa0', 'a href="VIDEO LINK"', 'Deleted video', 'a href="YOUTUBE CHANNEL LINK"'
            #'YouTube', 'Watched\xa0', 'a href="VIDEO LINK"', 'YouTube video name', 'a href="YOUTUBE CHANNEL LINK"'
            try:
                if(arr[i+4] == 'a href="https://www.youtube.com/channel/UCBR8-60-B28hp2BmDPdntcQ"'):
                    data[len(data)-1]['VideoName'] = arr[i+3]
                    data[len(data)-1]['VideoLink'] = arr[i+2][7:-1] #eliminates "" and 'a href ='
                else:
                    data[len(data)-1]['VideoLink'] = arr[i+3]
                    data[len(data)-1]['TimeStamp'] = timeConvert.TimeStamp(arr[i+4], timeZone)
            except:
                print('Error in Youtube Watch Data for len(4). Error Data:', arr[i:i+6], '\n')
        elif(len(currentEntry) == 2):
            #'Youtube', 'Watched a video that has been removed', 'TIMESTAMP'
            try:
                data[len(data)-1]['VideoName'] = 'Watched a video that has been removed'
                data[len(data)-1]['TimeStamp'] = timeConvert.TimeStamp(arr[i+2], timeZone)
            except:
                print('Error in Youtube Watch Data for len(2). Error Data:', arr[i:i+4], '\n')
    return data

def GoogleSearchHistory():
    """
    Data Format
    {
    'Product': 'Search', 
    'Action': None, 
    'Query (or site visited)': None,
    'TimeStamp' : TimeStamp Object
    }
    """
    checkDict = {'Products:', 'Search'}
    checkList = ['a href="https://www.google.com/search?q=', 'a href=']
    arr = parse('My Activity\Search\MyActivity.html', checkDict, checkList)
    if arr == None:
        return None
    data = []
    totalEntries = 0
    for i in range(len(arr)-3):
        currentPlace = i
        totalEntries += 1
        if 'Searched for\xa0hotels' in arr[i]:
            try:
                data.append({'Product': 'Search', 'Action': None, 'Query': None, 'TimeStamp': None, 'Type': None})
                data[len(data)-1]['Action'] = arr[currentPlace]
                data[len(data)-1]['TimeStamp'] = timeConvert.TimeStamp(arr[currentPlace + 1], timeZone)
                data[len(data)-1]['Type'] = arr[currentPlace + 2]
            except:
                print(arr[i], arr[i-3:i+4])
        elif 'Visited' in arr[i] or 'Searched for' in arr[i]:
            try:
                data.append({'Product': 'Search', 'Action': None, 'Query': None, 'TimeStamp': None, 'Type': None})
                data[len(data)-1]['Action'] = arr[currentPlace] #eliminates \xa0
                data[len(data)-1]['Query'] = arr[currentPlace + 1]
                data[len(data)-1]['TimeStamp'] = timeConvert.TimeStamp(arr[currentPlace + 2], timeZone)
                data[len(data)-1]['Type'] = arr[currentPlace + 3]
            except:
                print(arr[i], arr[i-3:i+4])
        elif 'Locations:' in arr[i]:
            try:
                data.append({'Product': 'Search', 'Action': None, 'Query': None, 'TimeStamp': None, 'Type': None}) #can update to better reflect map data
                data[len(data)-1]['Action'] = arr[i]
                data[len(data)-1]['Type'] = arr[i+1]
                data[len(data)-1]['Query'] = arr[i+2]
            except:
                print(arr[i], arr[i-3:i+4])
    return data