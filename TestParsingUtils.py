import unittest

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
        pass

    """Test stringToOutflows"""
    def test_stringToOutflows(self):
        pass

    """Test formatRawData"""
    def test_formatRawData(self):
        pass

    """Test checkValidInput"""
    def test_checkValidInput(self):
        pass

    """Test checkValidFile"""
    def test_checkValidFile(self):
        pass

    if __name__ == '__main__':
        unittest.main()
