import unittest
from DataUtils import *
from ParsingUtils import *
from PyCamellia import *

# a few variables for testing
expectedVars = getExpectedVars()
expectedData = getDataList()

class TestParsingUtils(unittest.TestCase):      
        
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


    """Test stringToInflows"""
    def test_stringToInflows(self):
        Points = [0.,1.,2.,-1.,-2.]
        (rawRegion, rawX, rawY) = expectedData["inflow"][0]
        (testRegion, testX, testY) = stringToInflows(rawRegion, rawX, rawY)
        expectedRegions = expectedData["inflowRegions"]
        expectedX = expectedData["inflowX"]
        expectedY = expectedData["inflowY"]     
        for i in Points:
            for j in Points:
                test = (i < 8)
                xAnsw = i * j
                yAnsw = i - j
                self.assertEqual(test, testRegion.matchesPoint(i,j))
                self.assertEqual(xAnsw, testX.evaluate(i,j))
                self.assertEqual(yAnsw, testY.evaluate(i,j))
           
     
    """Test stringToOutflows"""
    def test_stringToOutflows(self):
        Points = [0.,1.,2.,-1.,-2.]
        rawOutflow = expectedData["outflow"]
        testRegions = stringToOutflows(rawOutflow)
        expectedRegions = expectedData["outflowRegions"]    
        for i in Points:
            for j in Points:
                test = (i < 0)
                if(test != testRegions.matchesPoint(i,j)):
                    print "missmatch: "+str(i)+" "+str(j)
                self.assertEqual(test, testRegions.matchesPoint(i,j))
               
 
    """Test formatRawData"""
    def test_formatRawData(self):
        rawData = {}
        rawData["stokes"] = False
        rawData["reynolds"] = expectedData["reynolds"]
        rawData["transient"] = False
        rawData["meshDimensions"] = expectedData["rawDims"]
        rawData["numElements"] = expectedData["rawNumElements"]
        rawData["polyOrder"] = expectedData["polyOrder"]
        rawData["inflow"] = expectedData["inflow"]
        rawData["outflow"] = expectedData["outflow"]
        testData = formatRawData(rawData)        
                

    """Test checkValidInputWithValidData"""
    def test_checkValidInputWithValidData(self):
        validData = {}
        validData["stokes"] = False
        validData["transient"] = False
        validData["reynolds"] = 1000.0
        validData["meshDimensions"] = "1.0x1.0"
        validData["numElements"] = "3x5"
        validData["polyOrder"] = 3
        validData["inflow"] = expectedData["inflow"]
        validData["outflow"] = expectedData["outflow"]
        errors = checkValidInput(validData)        
     
        for field, result in errors.iteritems():
            print field + " " + str(result)
            self.assertFalse(result)


    """Test checkValidInputWithInvalidData"""
    def test_checkValidInputWithInvalidData(self):
        return
        invalidData = {}
        invalidData["stokes"] = ""
        invalidData["transient"] = ""
        invalidData["meshDimensions"] = expectedData["rawDims"]
        invalidData["numElements"] = expectedData["rawNumElements"]
        invalidData["polyOrder"] = expectedData["polyOrder"]
        invalidData["inflow"] = expectedData["inflow"]
        invalidData["outflow"] = expectedData["outflow"]
        errors = checkValidInput(invalidData)        
        
        for field, result in errors.iteritems():
            self.assertTrue(result)


    """Test checkValidFile"""
    def test_checkValidFile(self):
        checkValidFile("ParsingUtils.py")
                

    if __name__ == '__main__':
        unittest.main()
