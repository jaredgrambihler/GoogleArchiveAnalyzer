from GoogleArchive import timeConvert
import datetime                         #Datetime on plots
import os                               #Get current directory
import matplotlib.pyplot as plt         #Create and save plots
import matplotlib.dates as mdates       #Use datetime objects on plot


def freqHours(data, title, dir):
    """
    Saves a histogram for the frequency of the given data binned by each hour.
    Args:
        Data: A list of hours (Integers 1-24)
        Title: String for use in title. Title will be 'Frequency of [Title] (by hour)'
        Dir: Directory to save output to. Saved at current working directory with given Dir appended.
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
    """
    Saves a scatterplot of the given data with the value at each point specified by the sum of data
    for that given interval (e.g. number of searches a month for each month)
    Args:
        Data: A list of dictionaries that contain a 'TimeStamp' entry.
              These 'TimeStamp' entries should be of type TimeStamp as defined in timeConvert.
        Interval: String representing time to group data by. Can be day, month, or year (case insensitive)
        Title: String to be used in title of the output plot. Title will be '[Title] Usage Per [Interval]'
        Dir: Directory to save output to. Saved at current working directory with given Dir appended.
    """
    interval = interval.lower()
    if(interval not in {'day', 'month', 'year'}):
        print('Invalid plotting arguments for Audio Usage Plot')
        return 0
    dates = {}
    month = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4,'May':5,'Jun':6,'Jul':7,
             'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
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
    """
    Saves a histogram of frequency of the data by day of the week
    Args:
        Data: List of days of the week, as defined in datetime
        Title: String to be used in title. Title will be 'Frequency of [title] (by day of week)'
        Dir: Directory to save output to. Saved at current working directory with given Dir appended.
    """
    plt.hist(data, bins=7)
    plt.title('Frequency of ' + title + ' (by day of the week)')
    plt.xlabel('Day of the Week')
    plt.ylabel('Frequency(Cumulative, All Time)')
    plt.tight_layout()
    plt.savefig(os.getcwd() + dir + 'Frequency of ' + title + ' (by day of the week)')
    plt.close()


def displayDataPlots(data, freq = 'month', title = None, dir = ''):
    """
    Saves frequency by hour histogram, frequency by day of the week histogram,
    and a scatterplot of the frequency of the data over time.
    Prints information about data totals to console while running

    Args:
	    Data: List of dictionaries. Dictionaries should contain 'Product', 'TimeStamp' and 'Action' entries.
		      This dictionary storage format is defined in parse. Data returned from parse is compatible
	    Freq (optional): String, default 'month'. Frequency to be used for the frequency plot of data over time. 
		      Can be day, month, or year (case insensitive)
	    Title (optional): Stirng of title to be used in graphs. None by default. If this is true, it will label the graphs
		       according to the product and action associated with it. If a String is passed in, it will save the graphs
		       using the given title to describe the data. (e.g. 'Frequency of [title] (by day of week)')
	    Dir (optional): Directory to save output to. Saved at current working directory with given Dir appended. 
		     Empty string by default.
    """
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