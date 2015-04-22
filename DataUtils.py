from PyCamellia import *
from FormUtils import *
from InputData import *
from FormUtils import *

"""
A class of utility functions for generating data to
be used in test code. 
"""

# data, all in one place so it can be altered conveniently
data = {}
data["reynolds"] = 1000.0
data["numElements"] = [2,2]
data["polyOrder"] = 3
data["meshDimensions"] = [1.0,1.0]
data["numInflows"] =  1
data["inflwoRegions"] = "x<8"
data["inflowX"] = "4"
data["inflowY"] = "9"
data["numOutflows"] = 1
data["outflowRegions"] = "<0"
data["numWalls"] = 1
data["wallRegions"] = "y>9"

spaceDim = 2
useConformingTraces = True
mu = 1.0
x0 = [0.,0.]
delta_k = 1
dt = 0.1
x0 = [0.,0.]

"""
An accessor for data
This data includes everything but stokes, reynolds, and transient.
"""
def getDataList():
   return data

"""
Populate the given instance of InputData
with everything but stokes, reynolds, and transient.
"""
def populateInputData(inputData):
   for key, value in data.iteritems():
      if key != "reynolds":
         inputData.addVariable(key, value)

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
