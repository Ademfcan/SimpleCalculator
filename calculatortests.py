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
    assert calc.evaluate("10") == 10
    assert calc.evaluate("pi") == np.pi
    assert calc.evaluate("e") == np.e
    assert calc.evaluate("inf") == np.inf

    # unary operators
    assert calc.evaluate("cos(pi)") == -1
    assert calc.evaluate("sin(pi)") == 0
    assert calc.evaluate("tan(pi)") == 0

    # composition
    assert calc.evaluate("asin(sin(0))") == 0
    assert calc.evaluate("acos(cos(0))") == 0
    assert calc.evaluate("cos(1+1)") == np.cos(2)
    assert calc.evaluate("cos(sin(cos(sin(tan(2)))))") == np.cos(np.sin(np.cos(np.sin(np.tan(2)))))

if __name__ == "__main__":
    test()
