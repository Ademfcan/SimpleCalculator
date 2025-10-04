def _throwEquationSyntaxErrorWIndex(equation_input : str,  index : int, errorDescription : str = "error here"):
    raise SyntaxError(f"{equation_input} is not a valid equation!\n"+
                    f"{len(SyntaxError.__name__ + ": ") * " "}{"~"*index}^ {errorDescription}")