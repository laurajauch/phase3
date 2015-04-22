import re
import os.path

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

"""
Check to see if the given data is valid.
data: A dictionary containing the data to be tested
return: errors A dictionary mapping string description to boolean, 
False if field was valid, True if field was invalid
"""
def checkInputValidity(data):
    errors = {}
     

    # reynolds: must be a int and nStokes
    try:
        assert not (data["stokes"] and "reynolds" in data) # missmatch
        assert not data["stokes"] # nStokes
        assert int(data["reynolds"])
        errors["reynolds"] = False
    except:
        errors["reynolds"] = True

    # polyOrder: must be an int less than 10
    try:
        assert int(data["polyOrder"]) < 10
        assert int(data["polyOrder"]) > 0
        errors["polyOrder"] = False
    except:
        errors["polyOrder"] = True
        
    # numElements: int x int
    try:
        stringToElements(str(data["numElements"]))
        errors["numElements"] = False
    except:
        errors["numElements"] = True

    # meshDimensions: double x double
    try:
        stringToDims(str(data["meshDimensions"]))
        errors["meshDimensions"] = False
    except:
        errors["meshDimensions"] = True
            
    # inflowConditions: 
    try:
        stringToFilter(str(data["inflow"]))
        errors["inflow"] = False
    except:
        errors["inflow"] = True
                
    # outflowConditions:
    try:
        stringToFilter(str(data["outflow"]))
        errors["outflow"] = False
    except:
        errors["outflow"] = True
                    
    # loadFile: 
    try:
        os.path.isfile(str(data["loadFile"])) 
        errors["loadFile"] = False
    except:
        errors["loadFile"] = True


    return errors
