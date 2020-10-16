"""Currently a broken module.

Can't test this until there is purchase data to test on.

Writes all purchase data to a file.

If no data is found, no file is created.
Prints status of errors and numbers of files found while running.
"""
import os       #used for opening files and navigating directories
import json     #Used for loading the data from the files

def getData(path, dir):
    errorList = []  #track filenames that have errors occur
    fileCount = 0   #tracks number of files found in the directory
    merchants = {}  #dictionary of merchants. Each merchant is a key, value is # of purchases
    try:
        for file in os.listdir('../Takeout/Purchases _ Reservations'):
            fileCount += 1
            try:
                with open('..\Takeout\Purchases _ Reservations\\' + file, 'r', encoding='utf-8') as f:
                    fileDict = json.loads(f.read())
                    merchant = fileDict["transactionMerchant"]["name"]
                    if(merchant in merchants):
                        merchants[merchant] += 1 
                    else:
                        merchants[merchant] = 1
            except:
                errorList.append(file)
    except:
        print("Purchase data folder not found.") #Occurs when initial directory doesn't exist.
        return None;                             #Terminate function if the data isn't present!

    for fileName in errorList:
        print('Error in parsing for Purchase file: ' + fileName)
    if(fileCount > 0):
        with open(path + dir + 'PurchaseData.txt', 'w') as f:
            f.write('Total Number of Purchase files: ' + str(fileCount))
            f.write('\nPurchase Data Files By Merchant:')
            for merchant in merchants:
                f.write('\n    ' + merchant + ": " + str(merchants[merchant]))

    print('Total Number of Purchase files: ' + str(fileCount))