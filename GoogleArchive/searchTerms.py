
def commonSearchTerms(searchData, numTerms, path, dir):
    """Finds the numTerms number of most commonly searched terms across the searchData"""
    searchNums = {}
    for data in searchData:
        #get search
        search = getSearch(data)
        if(search):
            if search in searchNums:
                searchNums[search] += 1
            else:
                searchNums[search] = 1
    topSearches = []
    for search in searchNums:
        if(len(topSearches) < numTerms): #checks if list has been fully created
            if(len(topSearches) == 0): #first addition, no need to sort
                topSearches.append(search)
            else:
                for i in range(len(topSearches)): 
                    if searchNums[search] < searchNums[topSearches[i]]: #adds in smaller count before the larger value
                        topSearches.insert(i, search)
                        break
                    if(i == len(topSearches) - 1): #if at the end
                        topSearches.append(search)
        else: #if list is created, see if the new element should be added. If it can be, go down the list until it should be added
            for i in range(numTerms):
                if(i == numTerms - 1): #if it has gotten to the end of the list
                    topSearches.insert(i+1, search)
                    topSearches = topSearches[1:] #removes lowest count term 
                if(searchNums[search] > searchNums[topSearches[i]]): #if it is greater than the current index
                    if (searchNums[topSearches[i]] == searchNums[topSearches[i+1]]): #if the next index is the same, continue on to add later (because > it must be after all of the same)
                        pass
                    elif(searchNums[search] > searchNums[topSearches[i+1]]): #if it is also greater than the next index, continue on
                        pass
                    else:
                        topSearches.insert(i+1, search)
                        topSearches = topSearches[1:] #removes lowest count term 
                        break
                else: #if it is smaller than the first index, don't continue
                    break
    for i in range(len(topSearches)):
        topSearches[i] = [topSearches[i], searchNums[topSearches[i]]] #adds search nums into list
    logTopSearches(topSearches, path, dir)

def logTopSearches(topSearches, path, dir):
    f = open(path + dir + 'Common_Searches.txt', 'w')
    f.write('Top Searches:\n')
    for search in topSearches:
        f.write(str(search[0]) + ' , Frequency:' + str(search[1]) + '\n')
    f.close()


def getSearch(term):
    if(term['Product'] == 'Youtube' and term['Action'] == 'Search'):
        return term['Search'].lower() #uses lower to remove case sensitivity
    elif(term['Product'] == 'Search'):
        if('Searched for' in term['Action']):
            if(term['Query']): #handles for none query
                return term['Query'].lower()
        else:
            return None
    return None