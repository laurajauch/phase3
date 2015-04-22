import re
import os.path
import FunctionParser
import ConditionParser

"""
Some methods for formatting data input
"""
def stringToDims(inputstr):
    try:
        tokenList = re.split('x', inputstr)
        x = float(tokenList[0])
        y = float(tokenList[1])
        return [x,y]
    except:
        raise ValueError

def stringToElements(inputstr):
    try:
        tokenList = re.split('x', inputstr)
        x = int(tokenList[0])
        y = int(tokenList[1])
        return [x,y]
    except:
        raise ValueError

# the following 3 methods are not correct yet
def stringToInflows(rawRegions, rawYs, rawXs):
    numInflows = len(rawRegions)
    Regions = []
    Ys = []
    Xs = []
    i = 1
    success = [[0]*numInflows for i in range(3)]
    while i <= numInflows:
        try:
            Regions.append(stringToFilter(rawRegions[i]))
            success[0][i]=True
        except ValueError:
            pass
        try:
            Ys.append(stringToFilter(rawYs[i]))
            success[1][i]=True
        except ValueError:
            pass
        try:
            Xs.append(stringToFilter(rawXs[i]))
            success[2][i]=True
        except ValueError:
            pass
        self.addVariable("inflowRegions", Regions)
        self.addVariable("inflowX", Xs)
        self.addVariable("inflowY", Ys)
        return success

def stringToOutflows(rawRegions):
    Regions = []
    Ys = []
    Xs = []
    i = 1
    for region in rawRegions:
        try:
            Regions.append(stringToFilter(region))
        except ValueError:
            return False
        self.addVariable("outflowRegions", Regions)
        return True

def stringToWalls(datum): # not used?
    Regions = []
    i = 1
    for region in rawRegions:
        try:
            Regions.append(stringToFilter(region))
        except ValueError:
            return False
        self.addVariable("wallRegions", Regions)
        return True

def formatRawData(rawData):
    data ={}

    # stokes: boolean
    if rawData["stokes"] == "stokes":
        data["stokes"] = True
    else:
        data["stokes"] = False
        
    # reynolds: float/int
    data["reynolds"] = int(rawData["reynolds"])
    
    # transient: boolean
    if rawData["transient"] == "transient":
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
    regions = []
    xVel = []
    yVel = []
    for item in rawData["inflow"]:
        (region, x, y) = item
        regions.append(region)
        xVel.append(x)
        yVel.append(y)
    data["inflowRegions"] = regions
    data["inflowX"] = xVel
    data["inflowY"] = yVel
    
    # outflowRegions: string
    data["outflowRegions"] = rawData["outflow"]

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
        assert not rawData["stokes"] # nStokes
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
        for item in rawData["inflow"]:
            (condition, xVel, yVel) = item
            stringToFilter(str(condition))
            parseFunction(str(xVel))
            parseFunction(str(yVel)) 
        errors["inflow"] = False
    except:
        errors["inflow"] = True
                
    # outflow: strings (condition, xVelocity, yVelocity)
    try:
        for item in rawData["outflow"]:
            (condition, xVel, yVel) = item
            stringToFilter(str(condition))
            parseFunction(str(xVel))
            parseFunction(str(yVel))
        errors["outflow"] = False
    except:
        errors["outflow"] = True

"""
"""
def checkValidFile(filename):
    try:
        os.path.isfile(str(filename)) 
        return False
    except:
        return True
