import numpy as np


binaryoperators = {
    "+": {"p": 0, "f": np.add},
    "-": {"p": 0, "f": np.subtract},
    "*": {"p": 1, "f": np.multiply},
    "x": {"p": 1, "f": np.multiply},
    "/": {"p": 1, "f": np.divide},
    "%": {"p": 1, "f": lambda a, b : a % b},
    "^": {"p": 2, "f": np.pow},
}

unaryoperators = {
    "sin": {"f": np.sin},
    "cos": {"f": np.cos},
    "tan": {"f": np.tan},
    "log": {"f": np.log}
}

constants = {
    "pi": np.pi,
    "e": np.e,
    "eps": 1/np.inf,
    "inf": np.inf
}

negationChar = "-"

openSeparator = "("
closeSeparator = ")"
separators = {openSeparator, closeSeparator}