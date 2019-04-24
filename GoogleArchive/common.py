#contains shared functions for all files to use. 
#Should be imported into run.py to ensure it is available for all files to use.

import time

def parse(dir, checkDict, checkList):
    with open(dir, 'r', encoding='utf-8') as f:
        text= f.read()
        f.close()

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