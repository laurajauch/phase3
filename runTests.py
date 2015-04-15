from TestFormUtils import * 
import unittest

testSuite = unittest.makeSuite(TestFormUtils)
#testSuite.addTest(unittest.makeSuite(Test))

testRunner = unittest.TextTestRunner()

testRunner.run(testSuite)
