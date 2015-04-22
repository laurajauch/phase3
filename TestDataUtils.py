from PyCamellia import *
from DataUtils import *
from InputData import *
import unittest

class TestDataUtils(unittest.TestCase):

    """Test getDataList"""
    def test_getDataList(self):
        testData = getDataList()
        expectedData = {}
        expectedData["reynolds"] = 1000.0
        expectedData["numElements"] = [2,2]
        expectedData["polyOrder"] = 3
        expectedData["meshDimensions"] = [1.0,1.0]
        expectedData["numInflows"] =  1
        expectedData["inflwoRegions"] = "x<8"
        expectedData["inflowX"] = "4"
        expectedData["inflowY"] = "9"
        expectedData["numOutflows"] = 1
        expectedData["outflowRegions"] = "<0"
        expectedData["numWalls"] = 1
        expectedData["wallRegions"] = "y>9"
       
        for key, expectedValue in expectedData.iteritems():
            self.assertEqual(testData[key], expectedValue)
            
    """Test populateInputData"""
    def test_populateInputData(self):
        pass
        

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
    
    if __name__ == '__main__':
        unittest.main()
