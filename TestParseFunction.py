from PyCamellia import *
from FunctionParser import *
import unittest

class TestParseFunction(unittest.TestCase):

    """Test Add"""
    def test_add(self):
        func = parseFunction("1+x")
        for x in range(0,5):
            for y in range(0,5):
                answ = 1 + x
                self.assertEqual(answ, func.evaluate(x))

    """Test Subtract"""
    def test_subtract(self):
        func = parseFunction("3-x")
        for x in range(0,5):
            for y in range(0,5):
                answ = 3 - x
                self.assertEqual(answ, func.evaluate(x))

    """Test Divide"""
    def test_divide(self):
        func = parseFunction("10/x")
        for x in range(1,5):
            for y in range(1,5):
                answ = 10 / float(x)
                self.assertEqual(answ, func.evaluate(x))

    """Test Multiply"""
    def test_multiply(self):
        func = parseFunction("2*x")
        for x in range(0,5):
            for y in range(0,5):
                answ = 2 * x
                self.assertEqual(answ, func.evaluate(x))

    """Test Exonent"""
    def test_exponent(self):
        func = parseFunction("2^3")
        for x in range(0,5):
            for y in range(0,5):
                answ = 2 ** 3
                self.assertEqual(answ, func.evaluate(x))

    """Test Negative"""
    def test_negative(self):
        func = parseFunction("x+-2")
        for x in range(0,5):
            for y in range(0,5):
                answ = x + -2
                self.assertEqual(answ, func.evaluate(x))

    """Test ParenMultiply"""
    def test_parenMultiply(self):
        func = parseFunction("3(x)")
        for x in range(0,5):
            for y in range(0,5): 
                answ = 3 * x
                self.assertEqual(answ, func.evaluate(x))

    """Test XandY"""
    def test_xAndY(self):
        func = parseFunction("x+y")
        for x in range(0,5):
            for y in range(0,5): 
                answ = x + y
                self.assertEqual(answ, func.evaluate(x, y))

    """Test NoParens"""
    def test_noParens(self):
        func = parseFunction("5x^2y+2")
        for x in range(0,5):
            for y in range(0,5): 
                answ = 5 * (x**2) * y + 2
                self.assertEqual(answ, func.evaluate(x, y))

    """Test Doubles"""
    def test_doubles(self):
        func = parseFunction("2.0+5.0x*y^2")
        for x in range(0,5):
            for y in range(0,5): 
                answ = 2.0 + 5.0 * x * y**2
                self.assertEqual(answ, func.evaluate(x, y))

    """Test Parentheses 1"""
    def test_parantheses1(self):
        func = parseFunction("-3*(y-1)*(y-2)")
        for x in range(0,5):
            for y in range(0,5): 
                answ = -3*(y-1)*(y-2)
                self.assertEqual(answ, func.evaluate(x, y))

    #""Test Parentheses 2"""
    #def test_parantheses2(self):
        

    """Test HalfAssedDoubles"""
    def test_halfAssedDoubles(self):
        func = parseFunction("2.+.6-x^2+y")
        for x in range(0,5):
            for y in range(0,5): 
                answ = 2. + .6 - x**2 + y
                self.assertEqual(answ, func.evaluate(x, y))

    def testBasicRoberts(self):
        f_actual = parseFunction("-3*(y-1)*(y-2)")
        y = Function.yn(1)
        f_expected = -3*(y-1)*(y-2)
        testPoints = [[0,0],[0,1],[0,2],[1,3],[1,4],[1,5]]
        for point in testPoints:
            xVal = point[0]
            yVal = point[1]
            actualValue = f_actual.evaluate(xVal,yVal)
            expectedValue = f_expected.evaluate(xVal,yVal)
            tol = 1e-12
            if abs(actualValue-expectedValue) > tol :
                print "At (" + str(xVal) + "," + str(yVal) + "), expected ",
                print str(expectedValue) + ", but value was " + str(actualValue)
                self.assertAlmostEqual(f_actual.evaluate(xVal,yVal), f_expected.evaluate(xVal,yVal), delta=1e-12)

    def testBasicRoberts2(self):
        f_actual = parseFunction("3*(1-y)*(y-2)")
        y = Function.yn(1)
        f_expected = -3*(y-1)*(y-2)
        testPoints = [[0,0],[0,1],[0,2],[1,3],[1,4],[1,5]]
        for point in testPoints:
            xVal = point[0]
            yVal = point[1]
            self.assertAlmostEqual(f_actual.evaluate(xVal,yVal), f_expected.evaluate(xVal,yVal), delta=1e-12)

    def testBasicRoberts3(self):
        f_actual = parseFunction("-3*y*y+9*y-6")
        y = Function.yn(1)
        f_expected = -3*(y-1)*(y-2)
        testPoints = [[0,0],[0,1],[0,2],[1,3],[1,4],[1,5]]
        for point in testPoints:
            xVal = point[0]
            yVal = point[1]
            self.assertAlmostEqual(f_actual.evaluate(xVal,yVal), f_expected.evaluate(xVal,yVal), delta=1e-12)

    """Test ePowerOfTen"""
    """
    def test_ePowerOfTen(self):
        try:
            func = fp.parseFunction("xe2")
        except ValueError:
            error = True
        answ = x * 10 * 10
        #self.assertEqual(answ, func.evaluate(x))
        self.assertEqual(True, error)
        """

    if __name__ == '__main__':
        unittest.main()
