import os

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

def analyzeData(VoiceAndAudio = False):
    from GoogleArchive import parse, graph, purchase, photos
    if(VoiceAndAudio):
        from GoogleArchive import VoiceAndAudio #REQUIRES MUTAGEN

    purchase.getData(path, dir)
    photos.photoURL(path, dir)

    DriveData = parse.DriveHistory()
    YoutubeSearchData = parse.YoutubeSearchHistory()
    YoutubeWatchData = parse.YoutubeWatchHistory()
    GoogleSearchData = parse.GoogleSearchHistory()

    graph.displayDataPlots(YoutubeSearchData, dir = dir)
    graph.displayDataPlots(YoutubeWatchData, dir = dir)
    graph.displayDataPlots(GoogleSearchData, title = 'Google Search', dir = dir)

    allData = []
    allData.extend(YoutubeSearchData)
    allData.extend(YoutubeWatchData)
    allData.extend(GoogleSearchData)
    graph.displayDataPlots(allData, title = 'All Search and Watch', dir = dir)

#TODO - 
#parse chrome data
#parse maps
#parse location history
#number contacts?
#look into mail - after others are done