import os
import json

def getData(path, dir):
    errorList = []
    fileCount = 0
    merchants = {}
    try:
        for file in os.listdir('Purchases _ Reservations'):
            fileCount += 1
            try:
                with open('Purchases _ Reservations\\' + file, 'r', encoding='utf-8') as f:
                    fileDict = json.loads(f.read())
                    merchant = fileDict["transactionMerchant"]["name"]
                    if(merchant in merchants):
                        merchants[merchant] += 1 
                    else:
                        merchants[merchant] = 1
            except:
                errorList.append(file)
    except:
        print("Purchase data folder not found.")

    for fileName in errorList:
        print('Error in parsing for Purchase file: ' + fileName)

    with open(path + dir + 'PurchaseData.txt', 'w') as f:
        f.write('Total Number of Purchase files: ' + str(fileCount))
        f.write('\nPurchase Data Files By Merchant:')
        for merchant in merchants:
            f.write('\n    ' + merchant + ": " + str(merchants[merchant]))

    print('Total Number of Purchase files: ' + str(fileCount))