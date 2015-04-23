from PyCamellia import *
from FunctionParser import *
import unittest

fp = FunctionParser()

class TestParseFunction(unittest.TestCase):

    """Test Add"""
    def test_add(self):
        func = fp.parseFunction("1+x")
        for x in range(0,5):
            for y in range(0,5):
                answ = 1 + x
                self.assertEqual(answ, func.evaluate(x))

    """Test Subtract"""
    def test_subtract(self):
        func = fp.parseFunction("3-x")
        for x in range(0,5):
            for y in range(0,5):
                answ = 3 - x
                self.assertEqual(answ, func.evaluate(x))

    """Test Divide"""
    def test_divide(self):
        func = parseFunction("10/x")
        for x in range(0,5):
            for y in range(0,5):
                answ = 10 / x
                self.assertEqual(answ, func.evaluate(x))

    """Test Multiply"""
    def test_multiply(self):
        func = fp.parseFunction("2*x")
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
        func = fp.parseFunction("x+-2")
        for x in range(0,5):
            for y in range(0,5):
                answ = x + -2
                self.assertEqual(answ, func.evaluate(x))

    """Test ParenMultiply"""
    def test_parenMultiply(self):
        func = fp.parseFunction("3(x)")
        for x in range(0,5):
            for y in range(0,5): 
                answ = 3 * x
                self.assertEqual(answ, func.evaluate(x))

    """Test XandY"""
    def test_xAndY(self):
        func = fp.parseFunction("x+y")
        for x in range(0,5):
            for y in range(0,5): 
                answ = x + y
                self.assertEqual(answ, func.evaluate(x, y))

    """Test NoParens"""
    def test_noParens(self):
        func = fp.parseFunction("5x^2y+2")
        for x in range(0,5):
            for y in range(0,5): 
                answ = 5 * (x**2) * y + 2
                self.assertEqual(answ, func.evaluate(x, y))

    """Test Doubles"""
    def test_doubles(self):
        func = fp.parseFunction("2.0+5.0x*y^2")
        for x in range(0,5):
            for y in range(0,5): 
                answ = 2.0 + 5.0 * x * y**2
                self.assertEqual(answ, func.evaluate(x, y))

    """Test Parentheses 1"""
    def test_parantheses1(self):
        func = fp.parseFunction("-3*(y-1)*(y-2)")
        for x in range(0,5):
            for y in range(0,5): 
                answ = -3*(y-1)*(y-2)
                self.assertEqual(answ, func.evaluate(x, y))

    #""Test Parentheses 2"""
    #def test_parantheses2(self):
        

    """Test HalfAssedDoubles"""
    def test_halfAssedDoubles(self):
        func = fp.parseFunction("2.+.6-x^2+y")
        for x in range(0,5):
            for y in range(0,5): 
                answ = 2. + .6 - x**2 + y
                self.assertEqual(answ, func.evaluate(x, y))

    """Test ePowerOfTen"""
    def test_ePowerOfTen(self):
        try:
            func = fp.parseFunction("xe2")
        except ValueError:
            error = True
        answ = x * 10 * 10
        #self.assertEqual(answ, func.evaluate(x))
        self.assertEqual(True, error)

    if __name__ == '__main__':
        unittest.main()
