import re
import os.path
from FunctionParser import *
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

"""
rawInflows: tuple containing strings region, x velocity, and y velocity
returns tuple containing a filter and two functions
"""
def stringToInflows(rawRegion, rawXvel, rawYvel): #(rawRegion, rawXvel, rawYvel)
    try:
        region = (ConditionParser.parseCondition(rawRegion))
    except Exception,e:
        print "Inflow 1: "+str(e)
        raise ValueError
        
    try:
        for items in rawXvel:
            xvel = (parseFunction(rawXvel))
    except Exception,e:
        print "Inflow 2: "+str(e)
        raise ValueError
    
    try:
        for items in rawYvel:
            yvel = (parseFunction(rawYvel))
    except Exception,e:
        print "Inflow 3: "+str(e)
        raise ValueError
    
    return (region, xvel, yvel)

"""
rawRegions: string representation of the region
returns the SpacialFilter for the outflow
"""
def stringToOutflows(rawRegions):
    try:
        ret = ConditionParser.parseCondition(rawRegions)
    except Exception,e:
        print "Outflow: "+str(e)
        raise ValueError
    return ret

"""
Precondition: data is valid
data: A dictionary containing the data to be tested (same raw data passed to checkValidInput)
return: data A dictionary mapping string description to appropriate data type
"""
def formatRawData(rawData):
    data ={}

    # stokes: boolean
    data["stokes"] = bool(rawData["stokes"])
           
    # reynolds: float/int
    if not data["stokes"]:
        data["reynolds"] = int(rawData["reynolds"])
    
    # transient: boolean
    data["transient"] = bool(rawData["transient"])
           
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
    inflow = []
    # NEED TO FIX
    for item in rawData["inflow"]:
        (region, x, y) = stringToInflows(*item)
        regions.append(region)
        xVel.append(x)
        yVel.append(y)
    data["inflowRegions"] = regions
    data["inflowX"] = xVel
    data["inflowY"] = yVel
    data["inflows"] = rawData["inflow"]

    
    # outflowRegions: string
    outflow = []
    for item in rawData["outflow"]:
        outflow.append(stringToOutflows(item))
    data["outflowRegions"] = outflow
    data["outflows"] = rawData["outflow"]
    
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

    # polyOrder: must be an int less than 10 and greater than 0
    try:
        assert (int(rawData["polyOrder"]) < 10)
        assert (int(rawData["polyOrder"]) > 0)
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
            
    # inflow strings [(condition, xVelocity, yVelocity)]
    try:
        if len(rawData["inflow"]) > 0:
            for item in rawData["inflow"]:
                stringToInflow(item)
        errors["inflow"] = False
    except:
        errors["inflow"] = True
                
    # outflow: strings [condition]
    try:
        if len(rawData["outflow"]) > 0:
            for item in rawData["outflow"]:
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
