"""
Currently not included in __init__
Module that gives data on the Voice and Audio data from a Google Archive. Prodivides the number of files and the time required to listen to all of them.
If errors are encountered with the files, the number of error files will be printed. Requires mutagen package to run.
"""
# dependent on mutagen
# dependent on all google audio files being of the mp3 format
# could add in time chart

import os, time, datetime
from mutagen.mp3 import MP3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

fileCount = 0
timeCount = 0
errorCount = 0
timeList = []

def addTime(fileName):
    #Google's filename time format - %Y-%m-%d_%H_%M_%S_millisecond_%Z
    timeStr = fileName[0:-12] + fileName[-8:-4]  #removes milliseconds and extension from fileName
    timeList.append( time.strptime(timeStr, "%Y-%m-%d_%H_%M_%S_%Z") )

#raises a fileNotFoundError if the folder cannot be discovered.
#this error should be checked for if used in a module.
try:
    for audioFile in os.listdir('Voice and Audio'):
        try:
            if(".mp3" in audioFile):
                addTime(audioFile)
                fileCount += 1
                audio = MP3("Voice and Audio\\" + audioFile)
                timeCount += audio.info.length
        except:
            errorCount += 1
except:
    raise FileNotFoundError

if (errorCount != 0):
    print("Number of file errors:", errorCount)
print("Number of Audio Files:", fileCount)
print("Time of all recordings:", int(timeCount // 60), "minutes",
      int(timeCount % 60), "seconds")

def freqPlot(interval):
    interval = interval.lower()
    if(interval != 'day' and interval != 'month' and interval != 'year'):
        print('Invalid plotting arguments for Audio Usage Plot')
        return 0
    dates = {}
    for date in timeList:
        if(interval == 'year'):
            dateTuple = (date.tm_year)
        elif(interval == 'month'):
            dateTuple = (date.tm_year, date.tm_mon)
        elif(interval == 'day'):
            dateTuple = (date.tm_year, date.tm_mon, date.tm_mday)
        if dateTuple in dates:
            dates[dateTuple] += 1
        else:
            dates[dateTuple] = 1

    xs = []
    ys = []
    for date in dates:
        if(interval == 'year'):
            xs.append(datetime.date(date, 1, 1))
        elif(interval == 'month'):
            xs.append(datetime.date(date[0], date[1], 1))
        elif(interval == 'day'):
            xs.append(datetime.date(date[0], date[1], date[2]))
        ys.append(dates[date])
    plt.plot_date(xs, ys)
    plt.xticks(rotation = 60)
    plt.title('Google Voice and Audio Usage Per ' + interval)
    plt.tight_layout()
    plt.show()

freqPlot('month')