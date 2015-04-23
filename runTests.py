#from TestFormUtils import * 
#from TestInputData import *
from TestDataUtils import *
from TestPlotter import *
#from TestModel import *
import unittest

testSuite = unittest.makeSuite(TestDataUtils)
testSuite.addTest(unittest.makeSuite(TestPlotter))
#testSuite.addTest(unittest.makeSuite(TestFormUtils))
#testSuite.addTest(unittest.makeSuite(TestInputData))
#testSuite.addTest(unittest.makeSuite(TestModel))

testRunner = unittest.TextTestRunner()

testRunner.run(testSuite)
