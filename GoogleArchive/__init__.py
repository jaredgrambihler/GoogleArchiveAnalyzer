"""
Initial setup done here.
Creates a directory to store data in if it doesn't already exist
"""

import os #Required for creation of directory to save output to
from . import parse, graph, purchase, photos, searchTerms #import other parts of package to be used

dir = '\GoogleArchiveData\\'
path = os.getcwd()
if os.path.exists(path + dir):
    print('Data directory already exists. Updated data will be written to ' + path + dir)
else:
    try:
        os.mkdir(path + dir)
        print('Created Directory. Data will be wrriten to ' + path + dir)
    except:
        print('Error in creating folder.')
        raise Exception

def analyzeData(takeoutPath = ""):
    """Do analysis of all data.

    Runs analysis of PhotoURL, Purchase Data
    Youtube search and watch, and google search

    Args:
        takeoutPath (str): Relative path to takeout folder
    """
    photos.photoURL(path, dir)
    purchase.getData(path, dir)

    import time
    start = time.time()
    YoutubeSearchData = parse.YoutubeSearchHistory(takeoutPath)
    print("Took {}s to parse youtube search".format(time.time() - start))
    start = time.time()
    YoutubeWatchData = parse.YoutubeWatchHistory(takeoutPath)
    print("Took {}s to parse youtube watch".format(time.time() - start))
    start = time.time()
    GoogleSearchData = parse.GoogleSearchHistory(takeoutPath)
    print("Took {}s to parse google search".format(time.time() - start))

    allData = []
    if (YoutubeSearchData):
        allData.extend(YoutubeSearchData)
        graph.displayDataPlots(YoutubeSearchData, dir = dir)
    if (YoutubeWatchData):
        allData.extend(YoutubeWatchData)
        graph.displayDataPlots(YoutubeWatchData, dir = dir)
    if (GoogleSearchData):
        allData.extend(GoogleSearchData)
        graph.displayDataPlots(GoogleSearchData, title = 'Google Search', dir = dir)
    if(len(allData) > 0):
        graph.displayDataPlots(allData, title = 'All Search and Watch', dir = dir)

    searchTerms.commonSearchTerms(allData, 25, path, dir)

#TODO - 
#parse chrome data
#parse maps
#parse location history
#number contacts
#mail