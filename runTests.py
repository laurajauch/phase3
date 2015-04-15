from TestFormUtils import * 
from TestInputData import *
import unittest

testSuite = unittest.makeSuite(TestFormUtils)
testSuite.addTest(unittest.makeSuite(TestInputData))

testRunner = unittest.TextTestRunner()

testRunner.run(testSuite)
