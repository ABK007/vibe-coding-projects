"""
Quick test to verify calculator functions work as expected.
"""
import calculator

def test_all_operations():
    """Test all calculator operations."""
    print("Testing all calculator operations...")
    
    # Test basic operations
    assert calculator.add(2, 3) == 5
    assert calculator.subtract(5, 3) == 2
    assert calculator.multiply(4, 3) == 12
    assert calculator.divide(10, 2) == 5
    
    # Test advanced operations
    assert calculator.power(2, 3) == 8
    assert calculator.modulo(10, 3) == 1
    
    # Test edge cases
    assert calculator.add(-1, 1) == 0
    assert calculator.multiply(0, 100) == 0
    assert calculator.power(5, 0) == 1
    
    print("All tests passed!")

if __name__ == "__main__":
    test_all_operations()