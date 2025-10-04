import numpy as np
from calculator import build_basic_calc

def test_calculator():
    calc = build_basic_calc()

    # basic binary operations
    assert calc.calculate("1+1") == 2
    assert calc.calculate("1*1") == 1
    assert calc.calculate("1*1") == calc.calculate("1x1")
    assert calc.calculate("1^1") == 1
    assert calc.calculate("2^8") == 256
    
    # constant evaluations
    assert calc.calculate("10") == 10, "10 failed"
    assert calc.calculate("pi") == np.pi, "pi failed"
    assert calc.calculate("e") == np.e, "e failed"
    assert calc.calculate("inf") == np.inf, "inf failed"

    # unary operators
    assert calc.calculate("cos(pi)") == -1, "cos(pi) failed"
    assert calc.calculate("sin(pi)") == 0, "sin(pi) failed"
    assert calc.calculate("tan(pi)") == 0, "tan(pi) failed"
    assert calc.calculate("1+1*3(-5)") == -1, "Sneaky Parens failed"
    assert calc.calculate("1+1*3*(-5)") == -14, "Sneaky Parens failed"

    # composition
    assert calc.calculate("asin(sin(0))") == 0, "asin(sin(0)) failed"
    assert calc.calculate("acos(cos(0))") == 0, "acos(cos(0)) failed"
    assert calc.calculate("cos(1+1)") == np.cos(2), "cos(1+1) failed"
    assert calc.calculate("cos(sin(cos(sin(tan(2)))))") == np.cos(np.sin(np.cos(np.sin(np.tan(2))))), "cos(sin(cos(sin(tan(2))))) failed"

