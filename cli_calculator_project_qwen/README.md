# Interactive Calculator

A command-line calculator that supports basic and advanced arithmetic operations.

## Features

- Basic operations: addition (+), subtraction (-), multiplication (*), division (/)
- Advanced operations: exponentiation (** or ^), modulo (%)
- Interactive command-line interface
- Error handling for invalid inputs and division by zero
- Clean, formatted output

## Usage

To start the calculator, run:

```bash
python calculator.py
```

Then follow the prompts to enter calculations in the format: `number operator number`

Examples:
- `2 + 3`
- `10 * 5`
- `8 / 2`
- `2 ** 3` (2 to the power of 3)
- `10 % 3` (remainder of 10 divided by 3)

Type `quit` to exit the calculator.

## Running Tests

To run the unit tests:

```bash
python -m unittest test_calculator.py
```

## Supported Operations

- `+` : Addition
- `-` : Subtraction
- `*` : Multiplication
- `/` : Division
- `**` or `^` : Exponentiation
- `%` : Modulo (remainder)

## Error Handling

- Division by zero raises an error
- Invalid input formats are handled gracefully
- Invalid numbers are caught and reported
- Unknown operators are handled with helpful messages

## File Structure

- `calculator.py` - Main calculator module with functions and CLI interface
- `test_calculator.py` - Unit tests for calculator functions
- `test_interactive.py` - Additional test file

## Example Session

```
Welcome to the Calculator!
Supported operations: +, -, *, /, **, %
Type 'quit' to exit

Enter calculation (e.g., '2 + 3') or 'quit' to exit: 2 + 3
Result: 5

Enter calculation (e.g., '2 + 3') or 'quit' to exit: 10 / 3
Result: 3.3333333333333335

Enter calculation (e.g., '2 + 3') or 'quit' to exit: quit
Thank you for using the Calculator. Goodbye!
```