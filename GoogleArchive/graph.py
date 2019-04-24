from GoogleArchive import timeConvert
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

def freqHours(data, title, dir):
    """
    Takes in a list of hours and displays a histogram for the frequency of that data. Also takes in optional title.
    """
    plt.hist(data, bins = 24, range = (1,24))
    plt.title('Frequency of ' + title + ' (by hour)')
    plt.margins(x = 0, y = .15)
    plt.xlabel('Time of Day (24 Hour)')
    plt.ylabel('Frequency(Cumulative, All Time)')
    plt.tight_layout()
    plt.savefig(os.getcwd() + dir + 'Frequency of ' + title + ' (by hour)')
    plt.close()

def freqPlot(data, interval, title, dir):
    interval = interval.lower()
    if(interval != 'day' and interval != 'month' and interval != 'year'):
        print('Invalid plotting arguments for Audio Usage Plot')
        return 0
    dates = {}
    month = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12} #converts month strings to ints
    for item in data:
        if (item['TimeStamp'] != None):
            date = item['TimeStamp'].toDateTime(interval)
        if date in dates:
            dates[date] += 1
        else:
            dates[date] = 1 
    xs = []
    ys = []
    for date in dates:
        xs.append(date)
        ys.append(dates[date])
    plt.plot_date(xs, ys)
    plt.xticks(rotation = 60)
    plt.title(title + ' Usage Per ' + interval)
    plt.tight_layout()
    plt.savefig(os.getcwd() + dir + title + ' Usage Per ' + interval)
    plt.close()

def freqDays(data, title, dir):
    plt.hist(data, bins=7)
    plt.title('Frequency of ' + title + ' (by day of the week)')
    plt.xlabel('Day of the Week')
    plt.ylabel('Frequency(Cumulative, All Time)')
    plt.tight_layout()
    plt.savefig(os.getcwd() + dir + 'Frequency of ' + title + ' (by day of the week)')
    plt.close()


def displayDataPlots(data, freq = 'month', title = None, dir = ''):
    if title == None:
        print("Total " + data[0]['Product'] + ' ' + data[0]['Action'] + ": " + str(len(data)))
        times = timeConvert.getHours(data)
        freqHours(times, title = data[0]['Product'] + ' ' + data[0]['Action'] + ' Data', dir = dir)
        weeks = timeConvert.getWeeks(data)
        freqDays(weeks, title = data[0]['Product'] + ' ' + data[0]['Action'] + ' Data',  dir = dir)
        freqPlot(data, freq, data[0]['Product'] + ' ' + data[0]['Action'], dir = dir)
    else:
        print("Total " + title + ": " + str(len(data)))
        times = timeConvert.getHours(data)
        freqHours(times, title = title + ' Data', dir = dir)
        weeks = timeConvert.getWeeks(data)
        freqDays(weeks, title = title, dir = dir)
        freqPlot(data, freq, title = title, dir=dir)