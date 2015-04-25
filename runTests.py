from TestConditionParser import *
#from TestDataUtils import *
#from TestFormUtils import * 
#from TestInputData import *
#from TestModel import *
#from TestParseFunction import *
from TestParsingUtils import *
#from TestPlotError import *
#from TestPlotterP import *
#from TestPlotter import *
#from TestPlotterStream import *
import unittest

testSuite = unittest.makeSuite(TestConditionParser)
#testSuite.addTest(unittest.makeSuite(TestDataUtils))
#testSuite.addTest(unittest.makeSuite(TestFormUtils))
#testSuite.addTest(unittest.makeSuite(TestInputData))
#testSuite.addTest(unittest.makeSuite(TestModel))
#testSuite.addTest(unittest.makeSuite(TestParseFunction))
testSuite.addTest(unittest.makeSuite(TestParsingUtils))
#testSuite.addTest(unittest.makeSuite(TestPlotError))
#testSuite.addTest(unittest.makeSuite(TestPlotterP))
#testSuite.addTest(unittest.makeSuite(TestPlotter))
#testSuite.addTest(unittest.makeSuite(TestPlotterStream))



testRunner = unittest.TextTestRunner()

testRunner.run(testSuite)
