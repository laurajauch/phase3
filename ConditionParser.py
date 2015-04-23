from PyCamellia import *
delta_k = 1

def parseCondition(inputstr):
    i = 0
    xFirst = True
    noComma = True
    #if inputstr.count(',') > 1:
        #raise ValueError("Too many arguments in input.")
    for c in inputstr:
        if c == ',':
            noComma = False
            break
        i+=1
    if(noComma):
        if(inputstr[0] == 'x'):
            #print(inputstr[2:])
            xBounds = setXBoundary(inputstr)
            return xBounds
        elif(inputstr[0] == 'y'):
            #print(inputstr[2:])
            yBounds = setYBoundary(inputstr)
            return yBounds
        else:
            reject(inputstr[0]+" is not a valid variable, must be x or y.")
    arguments = inputstr.split(",")
    filters = []
    for argument in arguments:
        if argument[0] == 'x':
            filters.append(setXBoundary(argument))
        elif argument[0] == 'y':
            filters.append(setYBoundary(argument))
        else:
            reject(argument[0]+" is not a valid variable, must be x or y.")
    startingFilter = filters.pop() 
    for filter in filters:
        startingFilter = SpatialFilter.intersectionFilter(startingFilter,filter)
    return startingFilter
    
            

def setXBoundary(inputstr):
    digits = float(inputstr[2:])
    #print("x "+str(digits))
    c = inputstr[1]
    #print c
    if not type(digits) == float: #Need to change to isLong or something similar
        reject(digits+"is not a valid number.")
    
    if c == '=':
        return SpatialFilter.matchingX(float(digits))
    elif c == '<':
        return SpatialFilter.lessThanX(float(digits))
    elif c == '>':
        return SpatialFilter.greaterThanX(float(digits))
    else:
        reject(c+"is not a valid operator, must be =, <, or >.")
    




def setYBoundary(inputstr):
    digits = float(inputstr[2:])
    #print("y "+str(digits))
    c = inputstr[1]
    #print c
    if not type(digits) == float: #Need to change to isLong or something similar
        reject(digits+"is not a valid number.")
    if c == '=':
        return SpatialFilter.matchingY(float(digits))
    elif c == '<':
        return SpatialFilter.lessThanY(float(digits))
    elif c == '>':
        return SpatialFilter.greaterThanY(float(digits))
    else:
        reject(c+"is not a valid operator, must be =, <, or >.")




def reject(msg):
    raise ValueError(msg)
