from ConditionParser import *
from ParseFunction import *
from FormUtils import *
from ParsingUtils import *

"""
The memento doesn't care about any of the data, it just passes it around
"""
class Memento:
    def __init__(self, dataMap):
        self.set(dataMap)
    def get(self):
        return self.dataMap
    def set(self, dataMap):
        self.dataMap = dataMap

"""
A class to bottle up and pass around the user's input data.
This class is also currently responsible for confirming that 
the input data is valid.
"""
class InputData:

    """
    Stokes: stokesTrue, transient, dims [], numElements[], mesh, 
    polyOrder, inflow tuple (numInflows, [inflow regions], 
    [x velocities], [y velocities]), outflow tuple (numOutflows, 
    [outflow regions]), wall tuple (numWalls, [wall regions])

    Navier Stokes: nStokesFalse, Reynolds, transient, dims[], 
    numElements[], mesh, polyOrder, inflow tuple, outflow tuple, wall tuple 
    """
    def __init__(self):
        self.vars = {}

# Memento ------------------------------------------    
    def createMemento(self):
        return Memento(self.vars)
    
    def setMemento(self, memento):
        self.vars = memento.get()

# Generic Variable ---------------------------------
    def setVariables(self, data):
        self.vars = data

    def addVariable(self, string, var):
        self.vars[string] = var
    
    def getVariable(self, string):
        try: 
            return self.vars[string]
        except:
            pass

# Form ---------------------------------------------
    def setForm(self, form):
        self.vars["form"] = form
    
    def getForm(self):
        try:
            return self.vars["form"]
        except:
            print("InputData does not contain form")

# not used -----------------------------------------
    def storeInflows(self, rawRegions, rawYs, rawXs):
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


	        
    def storeOutflows(self, rawRegions):
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

	        
    def storeWalls(self, datum):
	    Regions = []
	    i = 1
	    for region in rawRegions:
	        try:
	            Regions.append(stringToFilter(region))
	        except ValueError:
	            return False
	    self.addVariable("wallRegions", Regions)
	    return True

