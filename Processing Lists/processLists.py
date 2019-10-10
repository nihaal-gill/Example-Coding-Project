#1
def processList1(list):
    return [ ((i*i) if i<0 == 0 else (i*i)+1) for i in list]
    
#2
def processList2(inputList, specialItem, ignoreItems):
    return[('special') if (i == specialItem and specialItem not in ignoreItems) else (i) for i in inputList if(i not in ignoreItems)]
