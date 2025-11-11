"""
Interactive Calculator Module

This module provides basic and advanced arithmetic operations in an interactive CLI format.
Supports addition, subtraction, multiplication, division, exponentiation, and modulo operations.

Usage:
    Run this module directly to start the interactive calculator.
    Or import individual functions to use in other modules.

Functions:
    add(a, b) - Returns the sum of a and b
    subtract(a, b) - Returns the difference of a and b
    multiply(a, b) - Returns the product of a and b
    divide(a, b) - Returns the quotient of a and b
    power(a, b) - Returns a raised to the power of b
    modulo(a, b) - Returns the remainder of a divided by b
    calculator_loop() - Starts the interactive calculator
"""


def add(a, b):
    """Return the sum of a and b."""
    return a + b


def subtract(a, b):
    """Return the difference of a and b."""
    return a - b


def multiply(a, b):
    """Return the product of a and b."""
    return a * b


def divide(a, b):
    """Return the quotient of a and b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(a, b):
    """Return a raised to the power of b."""
    return a ** b


def modulo(a, b):
    """Return the remainder of a divided by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a % b


def calculator_loop():
    """Main calculator loop for interactive use."""
    print("Welcome to the Calculator!")
    print("Supported operations: +, -, *, /, **, %")
    print("Type 'quit' to exit")
    
    while True:
        try:
            user_input = input("\nEnter calculation (e.g., '2 + 3') or 'quit' to exit: ").strip()
            
            if user_input.lower() == 'quit':
                print("Thank you for using the Calculator. Goodbye!")
                break
            
            # Parse the input
            parts = user_input.split()
            if len(parts) != 3:
                print("Invalid format! Please enter calculation in format: number operator number")
                continue
            
            num1_str, operator, num2_str = parts
            
            try:
                num1 = float(num1_str)
                num2 = float(num2_str)
            except ValueError:
                print("Invalid numbers! Please enter valid numbers.")
                continue
            
            # Perform the operation
            if operator == '+':
                result = add(num1, num2)
            elif operator == '-':
                result = subtract(num1, num2)
            elif operator == '*':
                result = multiply(num1, num2)
            elif operator == '/':
                result = divide(num1, num2)
            elif operator == '**' or operator == '^':
                result = power(num1, num2)
            elif operator == '%':
                result = modulo(num1, num2)
            else:
                print(f"Unsupported operator '{operator}'. Supported: +, -, *, /, **, %")
                continue
            
            # Format the result appropriately
            # If the result is a whole number, display as integer
            if result == int(result):
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
        
        except KeyboardInterrupt:
            print("\n\nCalculator interrupted. Goodbye!")
            break
        except ValueError as e:
            if "Cannot divide by zero" in str(e) or "Cannot divide by zero" in str(e):
                print("Error: Cannot divide by zero!")
            else:
                print(f"Value error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    calculator_loop()