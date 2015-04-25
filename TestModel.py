from Model import *
import FormUtils
import unittest
from DataUtils import *
from ParsingUtils import *

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
        model.plot("Error", 1)
        
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

    """Test SaveStokes"""
    def test_saveStokes(self):
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

        model = Model()
        model.inputData.addVariable("form", form)
        model.inputData.addVariable("transient", False)
        model.inputData.addVariable("meshDimensions", dims)
        model.inputData.addVariable("numElements", numElements)
        model.inputData.addVariable("polyOrder",  polyOrder)
        model.inputData.addVariable("inflow",  [("x<8", "x*y", "x-y")])
        model.inputData.addVariable("outflow",  ["x<0"])
        model.inputData.addVariable("outflowRegions", stringToOutflows("x<0"))
        
        model.save("testLoadSaveStokes")

    """Test SaveNStokes"""
    def test_saveNStokes(self):
        spaceDim = 2
        useConformingTraces = True
        mu = 1.0
        polyOrder = 3
        delta_k = 1
        dims = [1.0, 1.0]
        numElements = [2,2]
        x0 = [0.,0.]
        re = 1000.0
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
        
        form = NavierStokesVGPFormulation(meshTopo, re, polyOrder, delta_k)
        form.addZeroMeanPressureCondition()
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()

        model = Model()
        model.inputData.addVariable("form", form)
        model.inputData.addVariable("reynolds", re)
        model.inputData.addVariable("transient", False)
        model.inputData.addVariable("meshDimensions", dims)
        model.inputData.addVariable("numElements", numElements)
        model.inputData.addVariable("polyOrder",  polyOrder)
        model.inputData.addVariable("inflow",  [("x<8", "x*y", "x-y")])
        model.inputData.addVariable("outflow",  ["x<0"])
        model.inputData.addVariable("outflowRegions", stringToOutflows("x<0"))
        
        model.save("testLoadSaveNStokes")

    """Test LoadValidStokes"""
    def test_loadValidStokes(self):
        model = Model()
        self.test_saveStokes()
        model.load("testLoadSaveStokes")

    """Test LoadValidNStokes"""
    def test_loadValidNStokes(self):
        model = Model()
        self.test_saveNStokes()
        model.load("testLoadSaveNStokes")
   
    """Test LoadInvalid"""
    def test_loadInvalid(self):
        try:
            model = Model()
            self.test_save()
            model.load("xyz")
            raise ValueError 
        except:
            return

    if __name__ == '__main__':
        pass
