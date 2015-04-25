from ParsingUtils import *
import FormUtils
import unittest

goodNSData = {"stokes": "nstokes", "transient": "steady", "reynolds": "800", "meshDimensions": "8 x 2", "numElements": "8x2", "polyOrder": "3", "inflow": [("x=0, y > 1", "-3*(y-1)*(y-2)", "0")], "outflow": ["x=30"]}

class TestParsingUtils(unittest.TestCase):
    
    """Test StringToDims"""
    def testStringToDims(self):
        self.assertEqual(stringToDims("0 x 43"), [0,43])
        self.assertEqual(stringToDims("9.2 x3 "), [9.2,3])
        self.assertEqual(stringToDims(".2x 3.8"), [.2,3.8])
    
    """Test StringToElements"""
    def testStringToElements(self):
        self.assertEqual(stringToElements("0 x 43"), [0,43])
        self.assertEqual(stringToElements("92 x3 "), [92,3])
        self.assertEqual(stringToElements("2x 38"), [2,38])
    
    """Test StringToInflows"""
    def testStringToInflows(self):
        pass
    
    """Test StringToOutflows"""
    def testStringToInflows(self):
        pass
    
    
    """Test FormatRawData"""
    def testFormatRawData(self):
        formattedData = formatRawData(goodNSData)
        self.assertFalse(formattedData["stokes"])
        self.assertFalse(formattedData["transient"])
        self.assertEqual(800, formattedData["reynolds"])
        self.assertEqual(8, formattedData["meshDimensions"][0])
        self.assertEqual(2, formattedData["meshDimensions"][1])
        self.assertEqual(8, formattedData["numElements"][0])
        self.assertEqual(2, formattedData["numElements"][1])
        self.assertEqual(3, formattedData["polyOrder"])
    
    """Test checkValidInput"""
    
    """Test checkValidFile"""
