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
polyOrderNum = 3
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
nStokesInputData = InputData()
nStokesInputData.storeStokes(nStokes)
stokesInputData = InputData()
stokesInputData.storeStokes(stokes)
form = steadyLinearInit(dims, numElements, polyOrderNum)
reynolds = Reynolds.Instance()
state = State.Instance()
meshDims = MeshDimensions.Instance()
elements = Elements.Instance()
polyOrder = PolyOrder.Instance()
inflow = Inflow.Instance()
outflow = Outflow.Instance()
walls = Walls.Instance()


"""
This class tests InputData's functions and Memento, as well as the 
nested state classes that are within InputData and their functions
"""
class TestInputData(unittest.TestCase):

    """Test Memento's get & set"""
    def test_mementoGetSet(self):
        inputData = InputData(stokes)
        memento = inputData.createMemento()
        dataMap = memento.get()
        self.assertIn("stokes", dataMap)
        self.assertNotIn("nStokes", dataMap)
        
        memento.set([nStokes])
        dataMap = memento.get()
        self.assertIn(nStokes, dataMap)
        self.assertNotIn(stokes, dataMap)




    """Test InputData's init"""
    def test_inputDataInit(self):
        inputData = InputData(stokes)
        self.assertIsNotNone(inputData)
        self.assertEqual(stokes, inputData.getVariable("stokes"))

    """Test InputData's setForm & getForm"""
    def test_inputDataSetGetForm(self):
        inputData = InputData(stokes)
        inputData.setForm(form)
        self.assertIs(form, inputData.getForm())

    """Test InputData's addVariable & getVariable"""
    def test_inputDataAddVariable(self):
        inputData = InputData(stokes)
        inputData.addVariable("transient", transient)
        self.assertEqual(stokes, inputData.getVariable("stokes"))
        self.assertEqual(transient, inputData.getVariable("transient"))

    """Test InputData's createMemento"""
    def test_inputDataCreateMemento(self):
        inputData = InputData(stokes)
        memento = inputData.createMemento()
        self.assertIsNotNone(memento)
        self.assertIn("stokes", memento.get())

    """Test InputData's setMemento"""
    def test_inputDataSetMemento(self):
        inputData = InputData(stokes)
        inputData.setForm(form)
        inputData.addVariable("transient", transient)
        inputData.addVariable("dims", dims)
        inputData.addVariable("numElements", numElements)
        inputData.addVariable("mesh", meshTopo)
        inputData.addVariable("polyOrder", polyOrder)
        memento = inputData.createMemento()
        
        newData = InputData(nStokes)
        newData.setMemento(memento)
        mementoNew = newData.createMemento()
        dataMap = memento.get()
        self.assertIs(inputData.getForm(), newData.getForm())
        self.assertIn("form", dataMap)
        self.assertIn("stokes", dataMap)
        self.assertNotIn("nStokes", dataMap)
        self.assertIn("transient", dataMap)
        self.assertIn("dims", dataMap)
        self.assertIn("numElements", dataMap)
        self.assertIn("mesh", dataMap)
        self.assertIn("polyOrder", dataMap)



  
    """Test getFunction"""
    def test_getFunction(self):
        data = []
        self.assertEqual(getFunction("undo", data), "undo")
        self.assertFalse(getFunction("not a function", data))
        self.assertTrue(getFunction("x^2",data))
        self.assertEqual(data[0].evaluate(3), 9)
        
    """Test getFilter"""
    def test_getFilter(self):
        data = []
        self.assertEqual(getFilter("undo", data), "undo")
        self.assertFalse(getFunction("not a filter", data))
        self.assertFalse(getFunction("x=9y>2.2", data))
        self.assertTrue(getFilter(" x = 1.8, y>   8", data))
        self.assertTrue(getFilter("x>3,y=9",data))
        self.assertTrue(data[0].matchesPoint(1.8, 900))
        self.assertFalse(data[1].matchesPoint(2,9))
        
        
    """Test stringToDims"""
    def test_stringToDims(self):
        dims = stringToDims("3.1x 5.0")
        self.assertEqual(dims[0],3.1)
        self.assertEqual(dims[1],5.0)
        self.assertRaises(ValueError, lambda: stringToDims("a x 7"))
        
    """Test stringToElements"""
    def test_stringToElements(self):
        elements = stringToElements("3 x 5")
        self.assertEqual(elements[0],3)
        self.assertEqual(elements[1],5)
        self.assertRaises(ValueError, lambda: stringToElements("bx7"))
        self.assertRaises(ValueError, lambda: stringToElements("7.0 x4.2"))
        
    if __name__ == '__main__':
        unittest.main()




