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
A class to collect the user's input data.
"""
class InputData:

    """
    stokes = boolean
    reynolds = float/int
    transient = boolean
    meshDimensions = [float, float]
    numElements = [int, int]
    polyOrder = int
    inflow = strings [(inflowRegions, inflowX, inflowY)]
    inflowRegions = SpatialFilter
    inflowX = SpatialFilter
    inflowY = SpatialFilter
    outflowRegions = SpacialFilter
    outflow = strings [outflowRegions]
    """
    def __init__(self):
        self.vars = {}

# Memento ------------------------------------------    
    def createMemento(self):
        return Memento(self.vars)
    
    def setMemento(self, memento):
        self.vars = memento.get()

# Variable Accessors & Mutators ---------------------
    def setVariables(self, data):
        self.vars = data

    def addVariable(self, string, var):
        self.vars[string] = var
    
    def getVariable(self, string):
        try: 
            return self.vars[string]
        except:
            pass
