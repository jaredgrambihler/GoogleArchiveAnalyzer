"""
Initial setup done here.
Creates a directory to store data in if it doesn't already exist
"""

import os #Required for creation of directory to save output to
from GoogleArchive import parse, graph, purchase, photos, searchTerms #import other parts of package to be used

dir = '\GoogleArchiveData\\'
path = os.getcwd()
if os.path.exists(path + dir):
    print('Data directory already exists. Updated data will be written to ' + dir + ' in your Takeout folder.')
else:
    try:
        os.mkdir(path + dir)
        print('Created Directory. Data will be wrriten to ' + dir + ' in your Takout folder.')
    except:
        print('Error in creating folder.')
        raise Exception


def analyzeData():
    """
    Function run to do analysis of all data.
    Runs analysis of PhotoURL, Purchase Data
    Youtube search and watch, and google search
    """
    photos.photoURL(path, dir)
    purchase.getData(path, dir)

    YoutubeSearchData = parse.YoutubeSearchHistory()
    YoutubeWatchData = parse.YoutubeWatchHistory()
    GoogleSearchData = parse.GoogleSearchHistory()

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