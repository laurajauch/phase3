from TestFormUtils import * 
#from TestInputData import *
from TestModel import *
import unittest

#testSuite = unittest.makeSuite(TestFormUtils)
#testSuite.addTest(unittest.makeSuite(TestInputData))
#testSuite.addTest(unittest.makeSuite(TestModel))
testSuite = unittest.makeSuite(TestModel)

testRunner = unittest.TextTestRunner()

testRunner.run(testSuite)
