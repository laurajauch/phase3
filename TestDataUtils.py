from PyCamellia import *
from DataUtils import *
from InputData import *
import unittest

# a few variables for testing
expectedVars = getExpectedVars()
expectedData = getDataList()

"""
Test each method from DataUtils
"""
class TestDataUtils(unittest.TestCase):

    """Test getDataList & getExpectedVars"""
    def test_getDataListAndExpectedVars(self):
        for key in expectedVars:
            self.assertIsNotNone(expectedData[key])
            
    """Test populateInputData"""
    def test_populateInputData(self):
        testInputData = InputData()
        populateInputData(testInputData)
                       
        for key in expectedVars:
            self.assertEqual(testInputData.getVariable(key), expectedData[key])
        

    """Test generateForm"""
    def test_generateForm(self):
        pass

    """Test generateFormStokesTransient"""
    def test_generateFormStokesTransient(self):
        pass

    """Test generateFormStokesSteady"""
    def test_generateFormStokesSteady(self):
        pass

    """Test generateFormNavierStokesSteady"""
    def test_generateFormNavierStokesSteady(self):
        pass
        testForm = generateFormNavierStokesSteady()
        
        dims = expectedData["dims"]
        numElements = expectedData["numElements"]
        x0 = expectedData["x0"]
        delta_k = expectedData["delta_k"]
        re = expectedData["reynolds"]
        polyOrder = expectedData["polyOrder"]
        meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements, x0)
        expectedForm = NavierStokesVGPFormulation(meshTopo, re, polyOrder, delta_k)
        expectedForm.addZeroMeanPressureCondition()
        expectedForm.solve()

        expectedMesh = form.solution().mesh()
        expectedEnergyError = form.solution().energyErrorTotal()
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()

        testMesh = foo.solution().mesh()
        testEnergyError = test.solution().energyErrorTotal()
        testElementCount = testMesh.numActiveElements()
        testGlobalDofCount = testMesh.numGlobalDofs()

        self.assertEqual(4, testElementCount, expectedElementCount)
        self.assertEqual(634, testGlobalDofCount, expectedGlobalDofCount)
        self.assertEqual(0.000, testEnergyError, expectedEnergyError)
    
    if __name__ == '__main__':
        unittest.main()
