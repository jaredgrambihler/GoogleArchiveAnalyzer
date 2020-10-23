"""Functions for graphing data."""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import datetime
import os
from pathlib import Path
from collections import Counter
from typing import Sequence, Optional

from . import timeConvert
from .historyElements import HistoryElement


def freqHours(data: Sequence[int], title: str, dir: Path):
    """Save a histogram for the frequency of the given data binned by each hour.

    Args:
        data: A list of hours (Integers 1-24)
        title: String for use in title. Title will be 'Frequency of [Title] (by hour)'
        dir: Directory to save output to.
    """
    times = timeConvert.getHours(data)
    plt.hist(times, bins = 24, range = (1,24))
    plt.title('Frequency of ' + title + ' (by hour)')
    plt.margins(x = 0, y = .15)
    plt.xlabel('Time of Day (24 Hour)')
    plt.ylabel('Frequency(Cumulative, All Time)')
    plt.tight_layout()
    plt.savefig(str(dir) + '/Frequency of ' + title + ' (by hour)')
    plt.close()


def freqPlot(data: Sequence[HistoryElement], interval: str, title: str, dir: Path):
    """Save a scatterplot of the given data.
    
    The value at each point specified by the sum of data for that given interval
    (e.g. number of searches a month for each month)

    Args:
        data: A Sequence of HistoryElements
        interval: String representing time to group data by. Can be day, month, or year (case insensitive)
        title: String to be used in title of the output plot. Title will be '[Title] Usage Per [Interval]'
        dir: Directory to save output to.
    """
    interval = interval.lower()
    dates = Counter()
    month = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4,'May':5,'Jun':6,'Jul':7,
             'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
    for item in data:
        if (item.timeStamp != None):
            date = item['TimeStamp'].toDateTime(interval)
        dates[date] += 1
    xs = [date for date in dates]
    ys = [dates[date] for date in dates]
    plt.plot_date(xs, ys)
    plt.xticks(rotation = 60)
    plt.title(title + ' Usage Per ' + interval)
    plt.tight_layout()
    plt.savefig(str(dir) + "/" + title + ' Usage Per ' + interval)
    plt.close()


def freqDays(data: Sequence[HistoryElement], title: str, dir: Path):
    """Save a histogram of frequency of the data by day of the week.

    Args:
        data (Sequence[HistoryElement]): data to be plotted by frequency
        title: String to be used in title. Title will be 'Frequency of [title]
            (by day of week)'
        dir: Directory to save output to.
    """
    weeks = timeConvert.getWeeks(data)
    plt.hist(weeks, bins=7)
    plt.title('Frequency of ' + title + ' (by day of the week)')
    plt.xlabel('Day of the Week')
    plt.ylabel('Frequency(Cumulative, All Time)')
    plt.tight_layout()
    plt.savefig(str(dir) + '/Frequency of ' + title + ' (by day of the week)')
    plt.close()


def displayDataPlots(data: Sequence[HistoryElement], freq: Optional[str] = 'month',
                     title: Optional[str] = None, dir: Optional[Path] = None) -> None:
    """Save plots for the given data.
    
    Plots frequency by hour histogram, frequency by day of the week histogram,
    and a scatterplot of the frequency of the data over time.
    Prints information about data totals to console while running

    Args:
        data (Sequence[HistoryElements]) : elements to be plotted.
        freq (str) (optional): String, default 'month'. Frequency to be used for the
            frequency plot of data over time. Can be 'day', 'month', or 'year'
            (case insensitive)
        title (str) (optional): Title to be used in graphs. None by default.
            If this is None, it will label the graphs according to the product
            and action associated with it. If title is None, all HistoryElements
            must be of the same product and action . If a String is passed in,
            it will save the graphs using the given title to describe the data.
            (e.g. 'Frequency of [title] (by day of week)').
        dir (Path) (optional): Directory to save output to. Current working
            directory if None.

    Raises:
        ValueError: if title is None but all HistoryElemtents are not of the same
            product and action, or if freq is not one of 'day', 'month', or 'year'
        TypeError: if any of the given arguments do not match the type hints
    """
    if dir is None:
        dir = Path.cwd()
    if not all(isinstance(x, HistoryElement) for x in data):
        raise TypeError("At least one element of data is not a HistoryElement")
    elif not isinstance(freq, str):
        raise TypeError("freq must be of type str")
    elif not isinstance(dir, Path):
        raise TypeError("dir must be of type Path")
    if title is None:
        products = Counter(x.product for x in data)
        actions = Counter(x.action for x in data)
        if len(products) > 1:
            raise ValueError("At least two types of products are present in data \
                              Products present counter: {}".format(products))
        elif len(actions) > 1:
            raise ValueError("At least two types of actions are present in data \
                              Actions present counter: {}".format(actions))
        title =  data[0]['Product'] + ' ' + data[0]['Action']
    if not isinstance(title, str):
        raise TypeError("title must be of type str")
    if freq not in {'day', 'month', 'year'}:
        raise ValueError("Freq must be either 'day', 'month', or 'year'")
    print("Total " + title + ": " + str(len(data)))
    freqHours(data, title = title + ' Data', dir = dir)
    freqDays(data, title = title, dir = dir)
    freqPlot(data, freq, title = title, dir=dir)