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
