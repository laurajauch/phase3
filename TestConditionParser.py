from PyCamellia import *
from ConditionParser import *
import unittest

Points = [0.,1.,2.,-1.,-2.]

class TestConditionParser(unittest.TestCase):

    """Test Only X Equals"""
    def test_OnlyXEquals(self):
        filter = stringToFilter("x=0")       
        for i in Points:
            for j in Points:
                x = (i == 0.0)
                self.assertEqual(x, filter.matchesPoint(i,j))

    """Test Only X Greater""" 
    def test_OnlyXGreater(self):
        filter = stringToFilter("x>0")       
        for i in Points:
            for j in Points:
                x = (i >= 0.0)
                self.assertEqual(x, filter.matchesPoint(i,j))
    
    """Test Only X Less""" 
    def test_OnlyXLess(self):
        filter = stringToFilter("x<0")       
        for i in Points:
            for j in Points:
                x = (i <= 0.0)
                self.assertEqual(x, filter.matchesPoint(i,j))

    """Test Only Y Equals"""
    def test_OnlyYEquals(self):
        filter = stringToFilter("y=0")       
        for i in Points:
            for j in Points:
                y = (j == 0.0)
                self.assertEqual(y, filter.matchesPoint(i,j))
    
    """Test Only Y Greater"""
    def test_OnlyYGreater(self):
        filter = stringToFilter("y>0")       
        for i in Points:
            for j in Points:
                y = (j >= 0.0)
                self.assertEqual(y, filter.matchesPoint(i,j))

    """Test Only Y Less"""
    def test_OnlyYLess(self):
        filter = stringToFilter("y<0")       
        for i in Points:
            for j in Points:
                y = (j <= 0.0)
                self.assertEqual(y, filter.matchesPoint(i,j))

    """Test XY"""
    def test_XY(self):
        filter = stringToFilter("x=0,y<0")       
        for i in Points:
            for j in Points:
                x = (i == 0.0)
                y = (j <= 0.0)
                self.assertEqual(x and y, filter.matchesPoint(i,j))

    """Test YX"""
    def test_YX(self):
        filter = stringToFilter("y=0,x>0")       
        for i in Points:
            for j in Points:
                x = (i >= 0.0)
                y = (j == 0.0)
                self.assertEqual(x and y, filter.matchesPoint(i,j))

    """Test Doubles"""
    def test_Doubles(self):
        filter = stringToFilter("x>0.0,y>0.0")       
        for i in Points:
            for j in Points:
                x = (i >= 0.0)
                y = (j >= 0.0)
                self.assertEqual(x and y, filter.matchesPoint(i,j))

    """Test Half-Doubles"""
    def test_HalfDoubles(self):
        filter = stringToFilter("x>0.,y>0.")       
        for i in Points:
            for j in Points:
                x = (i >= 0.0)
                y = (j >= 0.0)
                self.assertEqual(x and y, filter.matchesPoint(i,j))
        

    """Test on many arguments"""
    def test_ManyArgs(self):
        filter = stringToFilter("y=0,x>0,y=3")  
        for i in Points:
            for j in Points:
                x = (i >= 0.0)
                y1 = (j == 0.0)
                y2 = (j == 3.0)
                self.assertEqual(x and y1 and y2, filter.matchesPoint(i,j))

    """Test Out of Order input"""
    def test_OutOfOrder(self):
        error = False
        try:
            filter = stringToFilter("0=x")       
        except ValueError:
            error = True
        self.assertEqual(True,error)

    """Test No Commas between arguments"""
    def test_NoComma(self):
        error = False
        try:
            filter = stringToFilter("x=0 y<2")       
        except ValueError:
            error = True
        self.assertEqual(True,error) 
    
    """Multiple arguments"""
    def test_MultipleArgs(self):
        filter = stringToFilter("x>0,x<2,y<2")       
        for i in Points:
            for j in Points:
                x1 = (i >= 0.0)
                x2 = (i <= 2.0)
                y = (j <= 2.0)
                self.assertEqual(x1 and x2 and y, filter.matchesPoint(i,j))



    if __name__ == '__main__':
        unittest.main()
