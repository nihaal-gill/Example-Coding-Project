#returns if two words are neighbors by checking if they are the same length and differ from
#each other by only one character
def areNeighbors(word1, word2):
    if (len(word1) != len(word2)):
        return False
    diffCount = 0
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            diffCount = diffCount + 1
    return (diffCount == 1)


# return a list of words from wordList that are "neighbors" (as defined
# by areNeighbors) of word1
def getNeighborList(word1, wordList):
    result = []
    for word2 in wordList:
        if areNeighbors(word1, word2):
            result.append(word2)
    return result

#  returns a list of lists representing all the "neighbor sets" in given file of words
#  Each neighbor set is itself a list [word neighborList], where
#  neighborList is the list of all neighbors of word.
def generateAndSaveAllNeighborLists(wordList):
    neighborData = []
    for word1 in wordList:
            neighborList = getNeighborList(word1, wordList)
            neighborData.append([word1, neighborList])
    return neighborData

def getWordList(filename):
    result = []
    fileStream = open(filename, 'r')
    for line in fileStream:
        word = line.strip()
        if (len(word) >= 1):
            result.append(word)
    return result

def wordNeighborInfo(filename):
    wordList = getWordList(filename)
    neighborData = generateAndSaveAllNeighborLists(wordList)

    largestNeighborInfo = None
    lonelyWords = []

    numberOfNeighborLists = len(neighborData)
    sumAllNeighborListLengths = 0

    for neighborInfo in neighborData:
        word = neighborInfo[0]
        neighborList = neighborInfo[1]
        sumAllNeighborListLengths = sumAllNeighborListLengths + len(neighborList)

        if len(neighborList) == 0:
            lonelyWords.append(word)

        if (largestNeighborInfo == None) or (len(neighborList) > len(largestNeighborInfo[1])):
            largestNeighborInfo = neighborInfo

    print("There are {} 'lonely' words:".format(len(lonelyWords)))
    print("The average number of neighbors is {:.2f}.".format(sumAllNeighborListLengths / numberOfNeighborLists))
    print("\'{}' has the most neighbors - {} of them: ".format(largestNeighborInfo[0], len(largestNeighborInfo[1])),
          end='')
    for word in largestNeighborInfo[1][:-1]:
        print(word, end=", ")
    print(largestNeighborInfo[1][-1])
    print("")
    print("Next, you can query about the neighbors of any word you like.")
    print("(hit Return/Enter when you want to quit)")
    print()
    query = input("What word do you want to know about? ")
    while query != "":
        neighborList = None
        for neighborSet in neighborData:
            word = neighborSet[0]
            if word == query:
                neighborList = neighborSet[1]
                break
        if neighborList == None:
            print("\'{}' is not in the word list.".format(query))
        elif len(neighborList) == 0:
            print("\'{}' has no neighbors.".format(query))
        else:
            print("\'{}' has the {} neighbors: ".format(query, len(neighborList)), end='')
            for word in neighborList[:-1]:
                print(word, end=", ")
            print(neighborList[-1])
        query = input("What word do you want to know about? ")
    print('Goodbye!')
    return
