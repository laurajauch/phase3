from Model import *
import FormUtils
import unittest

model = Model()
goodNSData = {"stokes": "nstokes", "transient": "steady", "reynolds": "800", "meshDimensions": "8 x 2", "numElements": "8x2", "polyOrder": "3", "inflow": [("x=0, y > 1", "-3*(y-1)*(y-2)", "0")], "outflow": ["x=30"]}

class TestModel(unittest.TestCase):

    """Test Store Good Navier-Stokes Data"""
    def test_goodNSStore(self):
        (valid, errors) = model.testData(goodNSData)
        print(errors)
        self.assertTrue(valid)
    
    """Test Store Data"""
    
    """Test Solve"""
    
    """Test Refine"""
    
    """Test Plot"""
    
    """Test Save"""
    
    """Test Load"""
    
    """Test Reset"""
