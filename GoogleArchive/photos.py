"""
Writes all URLs for Google Photos to a file
"""
import os
import json

def photoURL(path, dir):
    """
    Creates an output file, Photo_URLs.txt based on the specified path.
    File contains URLs of all photos on Google Photos.
    Prints out failure to find folder and number of file and folder errors encounters.
    Args:
        path: String, Current working directory
        dir: String, subdirectory to store file at.
    """
    #Will ignore any folders/files that have an error. Prints out the
    #number of errors upon termination.
    folderErrors = 0
    fileErrors = 0
    f = open(path + dir + 'Photo_URLs.txt', 'w')
    try:
        for folder in os.listdir('../Takeout/Google Photos'):
            try: 
                for file in os.listdir('..\Takeout\Google Photos\\' + folder):
                    try:
                        if 'json' in file:
                            photoFile = open('..\Takeout\Google Photos\\' + folder + '\\' + file)
                            fileDict = json.loads(photoFile.read())
                            f.write(fileDict["url"] + '\n\n')
                    except:
                        fileErrors += 1
            except:
                folderErrors += 1
    except:
        print('Google photo folder not found')
    finally:
        f.close()

    if(fileErrors != 0):
        print("Google Photos File Errors: " + str(fileErrors))
    if(folderErrors != 0):
        print("Google Photos Folder Errors: " + str(folderErrors))