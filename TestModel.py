from Model import *
import FormUtils
import unittest

model = Model()
goodData = {"stokes": "nstokes", "transient": "steady", "reynolds": "800", "meshDimensions": "8 x 2", "polyOrder": "3", "inflowRegions": ["x=0, y > 1"], "inflowX": ["-3*(y-1)*(y-2)"], "inflowY": ["0"], "outflowRegions": ["x=30"]}

class TestModel(unittest.TestCase):

    """Test Store Good Navier-Stokes Data"""
    def test_goodNSStore(self):
        (valid, errors) = model.testData(goodData)
        self.assertTrue(valid)
    
    """Test Test Data"""
    
    """Test Store Data"""
    
    """Test Solve"""
    
    """Test Refine"""
    
    """Test Plot"""
    
    """Test Save"""
    
    """Test Load"""
    
    """Test Reset"""
