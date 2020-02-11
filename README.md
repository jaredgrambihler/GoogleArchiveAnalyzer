#Google Archive Analyzer
This is a project in Python intended to analyze and output data regarding anyone's data from Google.

Dependencies:
Python Standard Library (os, time, json, datetime)
Matplotlib


To get your data, go to [https://takeout.google.com/](https://takeout.google.com/)
You can select to download as much or as little data as you want, but this code will analyze the following (if it is available):

 - My Activity (specifically Google Search History)
 - YouTube (Search and Watch History)
 
 Once the data is downloaded, it will be in a zip folder titled something like "Takeout-20200210" (The 2020 02 10 part represents a date).  Inside the zip is a folder simply titled "Takeout". Extract this folder to a directory of your choosing.

Clone the repository to this same directory, so it should be as follows:

someDir/Takeout
someDir/GoogleArchiveAnalyzer

By running "run.py" in GoogleArchiveAnalyzer, a folder in the same directory should be created:

someDir/GoogleArchiveAnalyzer/GoogleArchiveData

This folder will contain the output(s) of all the data!
Outputs include:
 - **Frequency by month**
 - **Frequency by hour**
 - **Frequency by day of week**
 - Most common Searches
 
 Bold terms are shown for:
 - Google Search
 - YouTube Watch
 - YouTube Search 

Some Examples of outputs are shown below:
![](https://i.imgur.com/Ren3HAB.png)
![](https://i.imgur.com/2yEQqjN.png)


