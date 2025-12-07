CustomCalc
A small, customizable calculator for Python that lets you define your own operators, constants, and functions. Uses NumPy for math operations.

Install:
pip install customcalc

Example:
``` Python
from calculator import build_basic_calc
# default operators/expressions
calc = build_basic_calc()
print(calc.calculate("1 + 2 * 3")) # 7
print(calc.calculate("cos(pi / 3)")) # 0.5
print(calc.calculate("3! + 4")) # 10

# Custom operator example:
from calculator import CalculatorBuilder
import numpy as np

b = CalculatorBuilder()

b.addBinaryOperator("plus", 0, np.add)
b.addConstant("one", 1)
b.addConstant("two", 2)

calc = b.build()
print(calc.calculate("one plus two")) # equals three
```

License: MIT
