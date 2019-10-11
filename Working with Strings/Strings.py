def q1(inputString):
    if len(inputString) < 2:
        print('There is no third largest integer for this input.')
        return
    #print the largest letter from the string
    currentIndex = 0
    currentMaxChar = 'a'
    currentSecondMaxChar = 'a'
    currentThirdMaxChar = 'a'
    while currentIndex < len(inputString):
        currentChar = inputString[currentIndex]
        if (currentChar.lower() > currentMaxChar):
            currentMaxChar = currentChar
            currentSecondMaxChar = currentMaxChar
        if (currentChar < currentMaxChar):
            currentSecondMaxChar = currentChar
            currentThirdMaxChar = currentSecondMaxChar
        if (currentChar < currentSecondMaxChar):
            currentThirdMaxChar = currentSecondMaxChar
        currentIndex = currentIndex + 1

    maxLetterCount = 0
    for a in inputString:
        count = 0
        for b in inputString:
            if(a == b):
                count = count + 1
        if(count > maxLetterCount):
            maxLetterCount = count
            repeatLetter = a
    print('In {}, the largest letter is {}, the third largest letter is {}, and the most common letter is {}, occuring {} times.'.format(inputString,currentMaxChar,currentThirdMaxChar,repeatLetter,maxLetterCount))
    return
