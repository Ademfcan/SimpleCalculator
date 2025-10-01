import math
import numpy as np

""" ------------------------- User Editable Fields ------------------------- """

# one char only
binaryoperators = {
    "+": {"p": 0, "f": np.add},
    "-": {"p": 0, "f": np.subtract},
    "*": {"p": 1, "f": np.multiply},
    "x": {"p": 1, "f": np.multiply},
    "/": {"p": 1, "f": np.divide},
    "%": {"p": 1, "f": lambda a, b : a % b},
    "^": {"p": 2, "f": np.pow},
    # "or": {"p": 2, "f": lambda a, b : a or b},
    # "and": {"p": 2, "f": lambda a, b : a and b},
    # "xor": {"p": 2, "f": lambda a, b : int(a) ^ int(b)},
    # "implies": {"p": 2, "f": lambda a, b : int((not a) or b)},
}

unaryoperators = {
    "sin": {"f": np.sin},
    "Sin": {"f": np.sin},
    "cos": {"f": np.cos},
    "tan": {"f": np.tan},
    "log": {"f": np.log},
    "ln": {"f": np.log},
    "asin": {"f": np.asin},
    "acos": {"f": np.acos},
    "atan": {"f": np.atan},
    "sqrt": {"f": np.sqrt},
    "abs": {"f": np.abs},
    "neg": {"f": np.negative},
    "nand": {"f": lambda a : int(not a)},
}

constants = {
    "pi": np.pi,
    "e": np.e,
    "eps": 1/np.inf,
    "inf": np.inf
}

# calculator works with floating points only for simplicity
def factorialWrapper(input_f : float) -> float:
    if input_f % 1 == 0:
        input_f = int(input_f)
    # let it throw the normal error if not a float
    return float(math.factorial(input_f))

# one char only!
tailmodifiers = {
    "!": factorialWrapper,
}


""" ------------------------- Please Dont Modify! ------------------------- """


negationChar = "-"

openSeparator = "("
closeSeparator = ")"
separators = {openSeparator, closeSeparator}


# assert binary operators are single char
# for binaryop in binaryoperators.keys():
#     if len(binaryop) > 1:
#         raise AssertionError(f"All Binary Operators must be one char only!\n{binaryop} is not!")

# assert tail modifiers are single char
for tailmodifier in tailmodifiers.keys():
    if len(tailmodifier) > 1:
        raise AssertionError(f"All Tail Modifiers must be one char only!\n{tailmodifier} is not!")
    
# everything else is free game