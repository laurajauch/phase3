from PyCamellia import *
from FormUtils import *
from InputData import *
from FormUtils import *

"""
A class of utility functions for generating data to
be used in test code. 
"""

# the variables expected in input data, used for testing
expectedVars = ["numElements", "polyOrder", "meshDimensions", "inflowRegions", "inflowX", "inflowY", "outflowRegions"]

# data, all in one place so it can be altered conveniently
data = {}
data["reynolds"] = 1000.0
data["numElements"] = [3,5]
data["rawNumElements"] = "3x5"
data["polyOrder"] = 3
data["meshDimensions"] = [3.1,5.0]
data["rawDims"] = "3.1x5.0"
data["rawInflows"] = [("x<8", "x*y", "x-y")] #raw
data["inflowRegions"] = ["x<8"]
data["inflowX"] = ["x*y"]
data["inflowY"] = ["x-y"]
data["rawOutflows"] = ["x<0"] #raw
data["outflowRegions"] = ["x<0"]
data["spaceDim"] = 2
data["useConformingTraces"] = True
data["mu"] = 1.0
data["x0"] = [0.,0.]
data["delta_k"] = 1
data["dt"] = 0.1
data["x0"] = [0.,0.]

"""
An accessor for expectedVars
This list includes all of the variables that are expected to
be present in InputData
"""
def getExpectedVars():
   return expectedVars

"""
An accessor for data
This data includes everything but stokes, and transient.
"""
def getDataList():
   return data

"""
Populate the given instance of InputData
with everything but stokes, reynolds, and transient.
"""
def populateInputData(inputData):
   for key, value in data.iteritems():
      if key in expectedVars:
         inputData.addVariable(key, value)
   #or just #inputData.setVars(data.iteritems()) ?

# nStokes, transient, or steady
def generateForm(kind):
   if kind == "nStokes":
      return generateFormNavierStokesSteady()
   if kind == "transient":
      return generateFormStokesTransient()
   if kind == "steady":
      return generateFormStokesSteady()

def generateFormStokesTransient():
   inputData = InputData()
   inputData.addVariable("stokes", True)
   inputData.addVariable("transient", True)
   populateInputData(inputData)
   return solve(inputData)

def generateFormStokesSteady():
   inputData = InputData()
   inputData.addVariable("stokes", True)
   inputData.addVariable("transient", False)
   populateInputData(inputData)
   return solve(inputData)

def generateFormNavierStokesSteady():
   inputData = InputData()
   inputData.addVariable("stokes", False)
   inputData.addVariable("reynolds", data["reynolds"])
   inputData.addVariable("transient", False)
   populateInputData(inputData)
   return solve(inputData)

if __name__ == '__main__':
   pass
