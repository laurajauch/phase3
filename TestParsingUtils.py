import unittest
from DataUtils import *
from ParsingUtils import *
from PyCamellia import *

# a few variables for testing
#expectedVars = getExpectedVars()
expectedData = getDataList()

class TestParsingUtils(unittest.TestCase):      
        
    """Test stringToDims"""
    def test_stringToDims(self):
        dims = stringToDims("3.1x 5.0")
        self.assertEqual(dims[0],3.1)
        self.assertEqual(dims[1],5.0)
        dims = stringToDims("31.2 x 0")
        self.assertEqual(dims[0],31.2)
        self.assertEqual(dims[1],0)
        self.assertRaises(ValueError, lambda: stringToDims("a x 7"))
        


    """Test stringToElements"""
    def test_stringToElements(self):
        elements = stringToElements("3 x 5")
        self.assertEqual(elements[0],3)
        self.assertEqual(elements[1],5)
        elements = stringToElements("82x9")
        self.assertEqual(elements[0],82)
        self.assertEqual(elements[1],9)
        self.assertRaises(ValueError, lambda: stringToElements("bx7"))
        self.assertRaises(ValueError, lambda: stringToElements("7.0 x4.2"))


    """Test stringToInflows"""
    def test_stringToInflows(self):
        Points = [0.,1.,2.,-1.,-2.]
        (rawRegion, rawX, rawY) = expectedData["rawInflows"][0]
        (testRegion, testX, testY) = stringToInflows(rawRegion, rawX, rawY)
        for x in Points:
            for y in Points:
                test = (x < 8)
                xAnsw = x * y
                yAnsw = x - y
                self.assertEqual(test, testRegion.matchesPoint(x,y))
                self.assertEqual(xAnsw, testX.evaluate(x,y))
                self.assertEqual(yAnsw, testY.evaluate(x,y))
           
     
    """Test stringToOutflows"""
    def test_stringToOutflows(self):
        Points = [0.1,1.,2.,-1.,-2.]
        rawOutflow = expectedData["rawOutflows"][0]
        testRegions = stringToOutflows(rawOutflow) # x<0
        for x in Points:
            for y in Points:
                test = (x < 0)
                if(test != testRegions.matchesPoint(x,y)):
                    print "missmatch: "+str(x)+" "+str(y)
                self.assertEqual(test, testRegions.matchesPoint(x,y))
               
 
    """Test formatRawData"""
    def test_formatRawData(self):
        rawData = {}
        rawData["stokes"] = False
        rawData["reynolds"] = expectedData["reynolds"]
        rawData["transient"] = False
        rawData["meshDimensions"] = expectedData["rawDims"]
        rawData["numElements"] = expectedData["rawNumElements"]
        rawData["polyOrder"] = expectedData["polyOrder"]
        rawData["inflows"] = expectedData["rawInflows"]
        rawData["outflows"] = expectedData["rawOutflows"]
        testData = formatRawData(rawData)
        self.assertFalse(testData["stokes"])
        self.assertEqual(testData["reynolds"], 1000)
        self.assertFalse(testData["transient"])
        self.assertEqual(testData["meshDimensions"][0], 3.1)
        self.assertEqual(testData["meshDimensions"][1], 5.0)
                

    """Test checkValidInputWithValidData"""
    def test_checkValidInputWithValidData(self):
        validData = {}
        validData["stokes"] = False
        validData["transient"] = False
        validData["reynolds"] = 1000.0
        validData["meshDimensions"] = "1.0x1.0"
        validData["numElements"] = "3x5"
        validData["polyOrder"] = 3
        validData["inflows"] = expectedData["rawInflows"]
        validData["outflows"] = stringToOutflows("x<0")
        errors = checkValidInput(validData)        
     
        for field, result in errors.iteritems():
            print field + " " + str(result)
            #self.assertFalse(result)


    """Test checkValidInputWithInvalidData"""
    def test_checkValidInputWithInvalidData(self):
        return
        invalidData = {}
        invalidData["stokes"] = ""
        invalidData["transient"] = ""
        invalidData["meshDimensions"] = 5 
        invalidData["numElements"] = 2
        invalidData["polyOrder"] = 11
        invalidData["inflows"] = ["6.0x6.9"]
        invalidData["outflows"] = ["5x6"]
        errors = checkValidInput(invalidData)        
        
        for field, result in errors.iteritems():
            self.assertTrue(result)


    """Test checkValidFile"""
    def test_checkValidFile(self):
        self.assertTrue(checkValidFile("ParsingUtils.py"))
        self.assertFalse(checkValidFile("xyz"))
                

    if __name__ == '__main__':
        unittest.main()
