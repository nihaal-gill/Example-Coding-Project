def q(num):
    newList = []
    index = 2
    while index <= num:
        potentialDivisor = index
        if(num % index == 0):
            if(numIsPrime(potentialDivisor)):
                newList.append(potentialDivisor)
                #print(newList)
        index = index + 1
    return(newList)

numTests = 0
def numIsPrime(n):
    global numTests
    isPrime = True
    potentialDivisor = 2
    while potentialDivisor < n:
        numTests = numTests + 1
        if (n % potentialDivisor) == 0:
            isPrime = False
        potentialDivisor = potentialDivisor + 1
    return isPrime
