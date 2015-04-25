from Model import *
import FormUtils
import unittest
from DataUtils import *

"""
Test each function in Model.py
"""
class TestModel(unittest.TestCase):

    """Test Refine"""
    def test_refine(self):
        pass
    
    """Test Plot"""
    def test_plot(self):
        model = Model()
        
        spaceDim = 2
        useConformingTraces = True
        mu = 1.0
        polyOrder = 3
        delta_k = 1
        dims = [1.0, 1.0]
        numElements = [2,2]
        x0 = [0.,0.]
        meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements, x0)
        
        topBoundary = SpatialFilter.matchingY(1.0)
        notTopBoundary = SpatialFilter.negatedFilter(topBoundary)
        x = Function.xn(1)
        rampWidth = 1./64
        H_left = Function.heaviside(rampWidth)
        H_right = Function.heaviside(1.0-rampWidth);
        ramp = (1-H_right) * H_left + (1./rampWidth) * (1-H_left) * x + (1./rampWidth) * H_right * (1-x)
        zero = Function.constant(0)
        topVelocity = Function.vectorize(ramp,zero)
        
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        
        model.inputData.addVariable("form", form)
        model.plot("Error")
        
    """Test Reset"""
    def test_reset(self):
        model = Model()
        populateInputData(model.inputData)
        self.assertTrue(model.inputData.vars) # dict evaluates to true when not empty
        model.reset()
        self.assertFalse(model.inputData.vars) # dict evaluates to false when empty

    """Test Solve"""
    def test_solve(self):
        pass

    """Test testData"""
    def test_testData(self):
        pass

    """Test storesData"""
    def test_storeData(self):
        pass

    """Test Save"""
    def test_save(self):
        pass

    """Test Load"""
    def test_load(self):
        pass
   

    if __name__ == '__main__':
        pass
