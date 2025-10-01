import numpy as np
from calculator import Calculator

def test():
    calc = Calculator()

    # basic binary operations
    assert calc.evaluate("1+1") == 2
    assert calc.evaluate("1*1") == 1
    assert calc.evaluate("1*1") == calc.evaluate("1x1")
    assert calc.evaluate("1^1") == 1
    assert calc.evaluate("2^8") == 256
    
    # constant evaluations
    assert calc.evaluate("10") == 10, "10 failed"
    assert calc.evaluate("pi") == np.pi, "pi failed"
    assert calc.evaluate("e") == np.e, "e failed"
    assert calc.evaluate("inf") == np.inf, "inf failed"

    # unary operators
    assert calc.evaluate("cos(pi)") == -1, "cos(pi) failed"
    assert calc.evaluate("sin(pi)") == 0, "sin(pi) failed"
    assert calc.evaluate("tan(pi)") == 0, "tan(pi) failed"
    assert calc.evaluate("1+1*3(-5)") == -1, "Sneaky Parens failed"
    assert calc.evaluate("1+1*3*(-5)") == -14, "Sneaky Parens failed"

    # composition
    assert calc.evaluate("asin(sin(0))") == 0, "asin(sin(0)) failed"
    assert calc.evaluate("acos(cos(0))") == 0, "acos(cos(0)) failed"
    assert calc.evaluate("cos(1+1)") == np.cos(2), "cos(1+1) failed"
    assert calc.evaluate("cos(sin(cos(sin(tan(2)))))") == np.cos(np.sin(np.cos(np.sin(np.tan(2))))), "cos(sin(cos(sin(tan(2))))) failed"

if __name__ == "__main__":
    test()
