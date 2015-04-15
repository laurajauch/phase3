from ConditionParser import *
from ParseFunction import *
from FormUtils import *
from ParsingUtils import *

# The memento doesn't care about any of the data, it just passes it around
class Memento:
    def __init__(self, dataMap):
        self.set(dataMap)
    def get(self):
        return self.dataMap
    def set(self, dataMap):
        self.dataMap = dataMap

class InputData:
    def __init__(self):
        self.vars = {} # to collect all the variables

        # Stokes: stokesTrue, transient, dims [], numElements[], mesh, 
        #   polyOrder, inflow tuple (numInflows, [inflow regions], [x velocities], [y velocities]),
        #   outflow tuple (numOutflows, [outflow regions]), wall tuple (numWalls, [wall regions])
        # Navier Stokes: nStokesFalse, Reynolds, transient, dims[], numElements[], mesh, polyOrder, 
        #   inflow tuple, outflow tuple, wall tuple

    def setForm(self, form):
        self.vars["form"] = form
    def getForm(self):
        try:
            return self.vars["form"]
        except:
            print("InputData does not contain form")
    def addVariable(self, string, var):
        self.vars[string] = var
    def getVariable(self, string):
        try: 
            return self.vars[string]
        except:
            pass
    def createMemento(self):
        return Memento(self.vars)
    def setMemento(self, memento):
        self.vars = memento.get()

	def storeReynolds(self, datum):
	    try:
	        self.addVariable("reynolds",int(datum))
	        return True
	    except ValueError:
	        return False

    def storeStokes(self, datum):
        try:
            self.addVariable("stokes", bool(datum)) #true for stokes, false for Nstokes
            return True
        except ValueError:
            return False
	
	def storeState(self, datum):
            try:
                datumL = datum.lower().strip()
                if datumL == "transient" or datumL == "steady state":
                    if datumL == "steady state":
                        self.addVariable("transient", False) # steady state
                        return True
                    elif (not self.getVariable("stokes")) and datumL == "transient":
                        print("Transient solves are not supported for Navier-Stokes")
                        return False
                    else:
                        self.addVariable("transient", True)
                        return True
                else:
                    return False
            except AttributeError:
                return False
	    
	def storeMeshDims(self, datum):
		try:
		    dims = stringToDims(str(datum).strip())
		    self.addVariable("meshDimensions", dims)
		    return True
		except ValueError:
		    return False
		
	def storeNumElements(self, inputData, datum):
		try:
		    numElements = stringToElements(str(datum).strip())
                    self.addVariable("numElements", numElements)
		    return True
		except ValueError:
		    return False
	    
	def storePolyOrder(self, inputData, datum):
		try:
			order = int(datum)
			if order <= 9 and order >= 1:
			    self.addVariable("polyOrder",order)
			    return True
			else:
			    return False
		except ValueError:
			return False
	    
	def storenumInflows(self, datum):
	    try:
	        self.addVariable("numInflows", int(datum))
	    except ValueError:
	        return False
	        
	def storeInflows(self, rawRegions, rawYs, rawXs):
	    Regions = []
	    Ys = []
	    Xs = []
	    i = 1
	    while i <= self.numInflows:
	        try:
	            Regions.append(stringToFilter(rawRegions[i]))
	        except ValueError:
	            return False
	        try:
	            Ys.append(stringToFilter(rawYs[i]))
	        except ValueError:
	            return False
	        try:
	            Xs.append(stringToFilter(rawXs[i]))
	        except ValueError:
	            return False
	    self.addVariable("inflowRegions", Regions)
	    self.addVariable("inflowX", Xs)
	    self.addVariable("inflowY", Ys)
	    return True
	    
	    
    def storenumOutflows(self, datum): #not used?
	    try:
	        self.addVariable("numOutflows", int(datum))
	    except ValueError:
	        return False
	        
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
	    
    def storenumWalls(self, datum): #not used?
	    try:
	         inputData.addVariable("numWalls", int(datum))
	    except ValueError:
	        return False
	        
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

