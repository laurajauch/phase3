from PyCamellia import *
from InputData import *
import FormUtils
import unittest

"""
Lots of variables to be used throughout for consistency
"""
useConformingTraces = True
mu = 1.0
dims = [1.0,1.0]
numElements = [2,2]
x0 = [0.,0.]
meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
polyOrder = 3
delta_k = 1
re = 1000.0
transient = True
steadyState = False

topBoundary = SpatialFilter.matchingY(1.0)
notTopBoundary = SpatialFilter.negatedFilter(topBoundary)
x = Function.xn(1)
rampWidth = 1./64
H_left = Function.heaviside(rampWidth)
H_right = Function.heaviside(1.0-rampWidth);
ramp = (1-H_right) * H_left + (1./rampWidth) * (1-H_left) * x + (1./rampWidth) * H_right * (1-x)
zero = Function.constant(0)
topVelocity = Function.vectorize(ramp,zero)

stokes = "True"
nStokes = "False"

"""
This class tests InputData's functions and Memento, as well as the 
nested state classes that are within InputData and their functions
"""
class TestInputData(unittest.TestCase):

# Memento ------------------------------------------    

    """Test Memento's get & set"""
    def test_mementoGetSet(self):
        inputData = InputData()
        inputData.addVariable("stokes", stokes)
        memento = inputData.createMemento()
        dataMap = memento.get()
        self.assertIn("stokes", dataMap)
        self.assertNotIn("nStokes", dataMap)
        
        memento.set([nStokes])
        dataMap = memento.get()
        self.assertIn(nStokes, dataMap)
        self.assertNotIn(stokes, dataMap)

    """Test InputData's createMemento"""
    def test_inputDataCreateMemento(self):
        inputData = InputData()
        inputData.addVariable("stokes", stokes)
        memento = inputData.createMemento()
        self.assertIsNotNone(memento)
        self.assertIn("stokes", memento.get())

    """Test InputData's setMemento"""
    def test_inputDataSetMemento(self):
        inputData = InputData()
        inputData.addVariable("stokes", stokes)
        inputData.addVariable("transient", transient)
        inputData.addVariable("dims", dims)
        inputData.addVariable("numElements", numElements)
        inputData.addVariable("mesh", meshTopo)
        inputData.addVariable("polyOrder", polyOrder)
        memento = inputData.createMemento()
        
        newData = InputData()
        newData.addVariable("stokes", nStokes)
        newData.setMemento(memento)
        mementoNew = newData.createMemento()
        dataMap = memento.get()
        self.assertIn("stokes", dataMap)
        self.assertNotIn("nStokes", dataMap)
        self.assertIn("transient", dataMap)
        self.assertIn("dims", dataMap)
        self.assertIn("numElements", dataMap)
        self.assertIn("mesh", dataMap)
        self.assertIn("polyOrder", dataMap)


# Variable Accessors & Mutators ---------------------

    """Test InputData's addVariable & getVariable"""
    def test_inputDataAddVariable(self):
        inputData = InputData()
        inputData.addVariable("transient", transient)
        self.assertEqual(transient, inputData.getVariable("transient"))
        
    if __name__ == '__main__':
        unittest.main()




