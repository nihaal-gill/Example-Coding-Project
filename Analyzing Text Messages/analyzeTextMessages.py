def analyzeMessages(filename, minWordLengthToConsider = 5):
    hamDict = {}
    spamDict = {}
    hamCount = 0 #counts the number of messages for ham by counting the number of lines
    spamCount = 0 #counts the number of messages for spam by counting the number of lines
    numberOfWordsHam = 0 #counts the number of total words there are in all of the ham messages combined
    numberOfWordsSpam = 0 #counts the number of total words there are in all of the spam messages combined
    avgLengthHam = 0 #finds the average length of words in a ham message
    avgLengthSpam = 0 #finds the average length of words in a spam message
    uniqueHam = 0 #finds the amount of unique words there are in ham messages
    uniqueSpam = 0 #finds the amount of unique words there are in spam messages

    fileStream = open(filename, 'r')
    for line in fileStream:
        if line is not "\n":
            newline = line.strip('?!. ''\n')
            newline = newline.lower()
            lineAsList = newline.split()
            hamList = []
            spamList = []
            if(lineAsList[0] == 'ham'):
                hamCount += 1 #counts number of messages by counting lines
                lineAsList.pop(0)
                for ele in lineAsList:
                    hamList.append(ele.strip('?!.' '\n'))
                numberOfWordsHam += len(hamList) #counts the number of total words
                for element in hamList:
                    if(hamDict.get(element) == None):
                        hamDict[element] = 1
                    else:
                        hamDict[element] += 1
                        #hamDict[element] = hamDict.get(element) + 1
            else:
                spamCount += 1 #counts the number of messages by counting the amount of line
                lineAsList.pop(0)
                for ele in lineAsList:
                    spamList.append(ele.strip('?!.' '\n'))
                spamList = lineAsList
                numberOfWordsSpam += len(spamList) #counts the number of total words
                for element in spamList:
                    if(spamDict.get(element) == None):
                        spamDict[element] = 1
                    else:
                        spamDict[element] += 1
                        #spamDict[element] = hamDict.get(element) + 1

    #find unique words
    uniqueHam = (len(hamDict))
    uniqueSpam = (len(spamDict))

    #finds the top 12 occuring words
    topWordsHam = []
    index = 0
    sortedHamTuple = sorted(hamDict.items(), key=lambda item: item[1], reverse=True)
    for i in range(len(sortedHamTuple)):
        if(len(sortedHamTuple[i][0]) > minWordLengthToConsider and index < 12):
            topWordsHam.append(sortedHamTuple[i][0])
            index += 1

    topWordsSpam = []
    index = 0
    sortedSpamTuple = sorted(spamDict.items(), key=lambda item: item[1], reverse=True)
    for i in range(len(sortedSpamTuple)):
        if (len(sortedSpamTuple[i][0]) > minWordLengthToConsider and index < 12):
            topWordsSpam.append(sortedSpamTuple[i][0])
            index += 1

    #finds the average length of words in a message
    avgLengthHam = numberOfWordsHam / hamCount
    avgLengthSpam = numberOfWordsSpam / spamCount


    print("Here are some statistics for the ham and spam messages.")
    print("-----------------------------------------------------------------------")
    print("The total number of ham messages are {}.".format(hamCount))
    print("The total number of spam messages are {}.".format(spamCount))
    print("-----------------------------------------------------------------------")
    print("The total number of words in ham messages are {}.".format(numberOfWordsHam))
    print("The total number of words in spam messages are {}.".format(numberOfWordsSpam))
    print("-----------------------------------------------------------------------")
    print("The number of unique words in ham messages are {}.".format(uniqueHam))
    print("The number of unique words in spam messages are {}.".format(uniqueSpam))
    print("-----------------------------------------------------------------------")
    print("The average length of ham messages are {} words.".format(round(avgLengthHam,1)))
    print("The average length of spam messages are {} words.".format(round(avgLengthSpam,1)))
    print("-----------------------------------------------------------------------")
    print("The most occuring words from the ham messages: ")
    print(" ")
    for word in topWordsHam:
        print("The word {} occured {} with a frequency of {}%.".format(word,hamDict.get(word),round(hamDict.get(word)/hamCount,2)))
    print("------------------------------------------------------------------------")
    print("The most occuring words from the spam messages: ")
    print(" ")
    for word in topWordsSpam:
        print("The word {} occured {} with a frequency of {}%.".format(word,spamDict.get(word),round(spamDict.get(word)/spamCount,2)))

