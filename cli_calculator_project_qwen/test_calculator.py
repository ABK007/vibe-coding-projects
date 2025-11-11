"""
Tests for the calculator module.
"""
import unittest
import calculator


class TestCalculator(unittest.TestCase):
    """Test cases for calculator functions."""
    
    def test_add(self):
        """Test addition operation."""
        self.assertEqual(calculator.add(2, 3), 5)
        self.assertEqual(calculator.add(-1, 1), 0)
        self.assertEqual(calculator.add(-5, -5), -10)
    
    def test_subtract(self):
        """Test subtraction operation."""
        self.assertEqual(calculator.subtract(5, 3), 2)
        self.assertEqual(calculator.subtract(1, 1), 0)
        self.assertEqual(calculator.subtract(-5, -3), -2)
    
    def test_multiply(self):
        """Test multiplication operation."""
        self.assertEqual(calculator.multiply(3, 4), 12)
        self.assertEqual(calculator.multiply(-2, 3), -6)
        self.assertEqual(calculator.multiply(0, 100), 0)
    
    def test_divide(self):
        """Test division operation."""
        self.assertEqual(calculator.divide(10, 2), 5)
        self.assertEqual(calculator.divide(9, 3), 3)
        self.assertEqual(calculator.divide(-6, 2), -3)
    
    def test_power(self):
        """Test power operation."""
        self.assertEqual(calculator.power(2, 3), 8)
        self.assertEqual(calculator.power(5, 0), 1)
        self.assertEqual(calculator.power(3, 2), 9)
        self.assertEqual(calculator.power(-2, 2), 4)
    
    def test_modulo(self):
        """Test modulo operation."""
        self.assertEqual(calculator.modulo(10, 3), 1)
        self.assertEqual(calculator.modulo(15, 4), 3)
        self.assertEqual(calculator.modulo(7, 7), 0)
    
    def test_divide_by_zero(self):
        """Test division by zero raises ValueError."""
        with self.assertRaises(ValueError):
            calculator.divide(10, 0)
    
    def test_modulo_by_zero(self):
        """Test modulo by zero raises ValueError."""
        with self.assertRaises(ValueError):
            calculator.modulo(10, 0)


if __name__ == '__main__':
    unittest.main()