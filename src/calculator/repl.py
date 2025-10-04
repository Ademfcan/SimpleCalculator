import numpy as np
from .calculator import CalculatorBuilder, Calculator


def repl(c : Calculator):
    while True:
        input_str = input("Please enter your equation>>> ")
        try:
            result = c.calculate(input_str, debug=True)
            print(f"Result: {result}")
        except SyntaxError as e:
            print(f"Failed to parse input!: \n{e.__class__.__name__}: {e}")
        except KeyboardInterrupt as e:
            print("Exiting Program...")


def build_basic_calc() -> Calculator:
    b = CalculatorBuilder()
    
    b.addBinaryOperator("+", 0, np.add)
    b.addBinaryOperator("-", 0, np.subtract)
    b.addBinaryOperator("*", 1, np.multiply)
    b.addBinaryOperator("x", 1, np.multiply)
    b.addBinaryOperator("/", 1, np.divide)
    b.addBinaryOperator("%", 1, lambda a, b : a % b)
    b.addBinaryOperator("^", 2, np.power)

    b.addUnaryOperator("sin", np.sin)
    b.addUnaryOperator("cos", np.cos)
    b.addUnaryOperator("tan", np.tan)
    b.addUnaryOperator("log", np.log)
    b.addUnaryOperator("ln", np.log)
    b.addUnaryOperator("asin", np.asin)
    b.addUnaryOperator("acos", np.acos)
    b.addUnaryOperator("atan", np.atan)
    b.addUnaryOperator("sqrt", np.sqrt)
    b.addUnaryOperator("abs", np.abs)

    b.addConstant("pi", np.pi)
    b.addConstant("e", np.e)
    b.addConstant("eps", 1/np.inf)
    b.addConstant("inf", np.inf)

    b.addSuffixOperator("!", lambda input_f : float(np.math.factorial(int(input_f)) if input_f % 1 == 0 else np.math.factorial(input_f)))

    return b.build()

if __name__ == "__main__":
    repl(build_basic_calc())