import re
import os.path
from FunctionParser import *
from ConditionParser import *

"""
Some methods for formatting data input
"""
def stringToDims(inputstr):
    try:
        tokenList = re.split('x', inputstr)
        x = float(tokenList[0])
        y = float(tokenList[1])
        return [x,y]
    except Exception,e:
        print(str(e))
        raise ValueError

def stringToElements(inputstr):
    try:
        tokenList = re.split('x', inputstr)
        x = int(tokenList[0])
        y = int(tokenList[1])
        return [x,y]
    except Exception,e:
        print(str(e))
        raise ValueError

# the following 3 methods are not correct yet
"""
rawInflows: tuple containing strings region, x velocity, and y velocity
returns tuple containing a filter and two functions
"""
def stringToInflows((rawRegion, rawXvel, rawYvel)):
    try:
        region = parseCondition(rawRegion) 
    except:
        raise ValueError
        
    try:
        xvel = parseFunction(rawXvel) 
    except:
        raise ValueError
    
    try:
        yvel = parseFunction(rawYval) 
    except:
        raise ValueError
    
    return (region, xvel, yvel)

def stringToOutflows(rawRegions):
    Regions = []
    for region in rawRegions:
        try:
            Regions.append(parseCondition(region)) 
        except:
            raise ValueError
        return Regions

"""
Precondition: data is valid
data: A dictionary containing the data to be tested (same raw data passed to checkValidInput)
return: data A dictionary mapping string description to appropriate data type
"""
def formatRawData(rawData):
    data ={}

    # stokes: boolean
    if rawData["stokes"]:
        data["stokes"] = True
    else:
        data["stokes"] = False
        
    # reynolds: float/int
    if not data["stokes"]:
        data["reynolds"] = int(rawData["reynolds"])
    
    # transient: boolean
    if rawData["transient"]:
        data["transient"] = True
    else:
        data["transient"] = False
        
    # meshDimensions: [float, float]
    data["meshDimensions"] = stringToDims(rawData["meshDimensions"])

    # numElements: [int, int]
    data["numElements"] = stringToElements(rawData["numElements"])
    
    # polyOrder: int
    data["polyOrder"] = int(rawData["polyOrder"])
        
    # inflowRegions, inflowX, inflowY: string
    #regions = []
    #xVel = []
    #yVel = []
    inflow = []
    # NEED TO FIX
    #for item in rawData["inflow"]:
    #    (region, x, y) = item
    #    regions.append(region)
    #    xVel.append(x)
    #    yVel.append(y)
    #data["inflowRegions"] = regions
    #data["inflowX"] = xVel
    #data["inflowY"] = yVel
        #inflow.append(stringToInflows(item))
    data["inflow"] = inflow
    
    # outflowRegions: string
    outflow = []
    #for item in rawData["outflow"]:
        #outflow.append(stringToOutflows(item))
    data["outflow"] = outflow
    
    # wallRegions: string
    # ?
    return data

#--------------------------------------------------------------

"""
Check to see if the given data is valid.
data: A dictionary containing the data to be tested
return: errors A dictionary mapping string description to boolean, 
False if field was valid, True if field was invalid
"""
def checkValidInput(rawData):
    errors = {}
     

    # reynolds: must be a int and nStokes
    try:
        assert not (rawData["stokes"] and "reynolds" in rawData) # missmatch
        if not rawData["stokes"]:
            assert int(rawData["reynolds"])
        errors["reynolds"] = False
    except:
        errors["reynolds"] = True

    # polyOrder: must be an int less than 10
    try:
        assert int(rawData["polyOrder"]) < 10
        assert int(rawData["polyOrder"]) > 0
        errors["polyOrder"] = False
    except:
        errors["polyOrder"] = True
        
    # numElements: int x int
    try:
        stringToElements(str(rawData["numElements"]))
        errors["numElements"] = False
    except:
        errors["numElements"] = True

    # meshDimensions: double x double
    try:
        stringToDims(str(rawData["meshDimensions"]))
        errors["meshDimensions"] = False
    except:
        errors["meshDimensions"] = True
            
    # inflow strings (condition, xVelocity, yVelocity)
    try:
        if len(rawData["inflow"]) > 0:
            for item in rawData["inflow"]:
                #    (condition, xVel, yVel) = item
                #    stringToFilter(str(condition))
                #    parseFunction(str(xVel))
                #    parseFunction(str(yVel)) 
                stringToInflow(item)
        errors["inflow"] = False
    except:
        errors["inflow"] = True
                
    # outflow: strings (condition, xVelocity, yVelocity)
    try:
        if len(rawData["outflow"]) > 0:
            for item in rawData["outflow"]:
                #    (condition, xVel, yVel) = item
                #    stringToFilter(str(condition))
                #    parseFunction(str(xVel))
                #    parseFunction(str(yVel))
                stringToOutflow(item)
        errors["outflow"] = False
    except:
        errors["outflow"] = True
    
    return errors

"""
"""
def checkValidFile(filename):
    try:
        os.path.isfile(str(filename)) 
        return False
    except:
        return True
