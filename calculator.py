from typing import Optional

import numpy as np

operators = {
    "+": {"p": 0, "f": np.add},
    "-": {"p": 0, "f": np.subtract},
    "*": {"p": 1, "f": np.multiply},
    "x": {"p": 1, "f": np.multiply},
    "/": {"p": 1, "f": np.divide},
    "%": {"p": 1, "f": lambda a, b : a % b},
    "^": {"p": 2, "f": np.pow},
}

openSeparator = "("
closeSeparator = ")"
separators = {openSeparator, closeSeparator}

"""
a+b-c -> -+abc
(a+b)*c -> *+abc
a+b*c -> +a*bc
a^b+c*d -> ^ab+*cd
a^b*c+d -> ^ab+*cd
""" 

"""
 a+b-c

    (+)
  (a) (-)
     (b)(c)

 a+b*c

    (+)
  (a) (*)
     (b)(c)

 (a+b)*c

    (+ pl1)
  (a) (*)
     (b)(c)

 (a+(a+b))*c

    (+ p11)
  (a) (+ p12)
     (a)(*)
      (b)(c)
"""

def throwEquationSyntaxErrorWIndex(equation_input : str,  index : int, errorDescription : str = "error here"):
    raise SyntaxError(f"{equation_input} is not a valid equation!\n"+
                      f"{len(SyntaxError.__name__ + ": ") * " "}{"~"*index}^ {errorDescription}")


def process_input_str(input_str : str) -> list:
    # print(f"{input_str=}")
    output = []

    lastSpecialCharIdx = -1
    lastSpecialChar = ""
    for i in range(len(input_str)):
        c = input_str[i]

        is_special_subtr = c == "-" and (i == 0 or lastSpecialCharIdx == i-1)
        is_after_closing = (lastSpecialCharIdx == i-1 and lastSpecialChar == closeSeparator)
        is_before_open =  (lastSpecialCharIdx == i-1 and input_str[i] == openSeparator)

        if is_special_subtr and not is_after_closing:
            # case like "-1" or "...+-1" but NOT "...)-1"
            continue # treat as part of a number

        is_operator = c in operators.keys()

        if is_after_closing and is_operator:
            # case like "...)+a"
            output.append(c)
            lastSpecialChar = c
            lastSpecialCharIdx = i
            continue

        is_separator = c in separators

        if is_separator or is_operator:
            
            if i > 0 and not is_before_open:
                prev = input_str[lastSpecialCharIdx+1:i]
                # to avoid empty slices like ")+"
                if not prev:
                    throwEquationSyntaxErrorWIndex(input_str , i, "Multiple Operators in a row")

                output.append(prev) # number
            
            output.append(c) # operator            
            lastSpecialChar = c
            lastSpecialCharIdx = i

            
    # handle remaining argument
    # case like "1+2" or "(5+3)-1"
    # avoid case like "1+2+"
    if lastSpecialCharIdx < len(input_str) - 1:
        output.append(input_str[lastSpecialCharIdx+1:])
    elif input_str[lastSpecialCharIdx] in operators.keys():
        throwEquationSyntaxErrorWIndex(input_str, len(input_str)-1, "Last Value cannot be a operator!")

    # verify equation and convert input numbers to numbers
    lastOperator = -1
    separatorlevel = 0    
    errorIdx = 0
    for i in range(len(output)):
        val = output[i]
        errorIdx += len(val)
        
        if val in separators:
            # looking for even parentheses
            # eg "()" or ()() or (())"
            if val == openSeparator:
                separatorlevel+=1
            else:
                separatorlevel-=1
            continue

        if val not in operators.keys():
            # expected numeric, try conversion
            # convert to float
            try:
                number = float(val)
            except ValueError:
                throwEquationSyntaxErrorWIndex(input_str , errorIdx-1, f"Failed to convert: {output[i]}")

            output[i] = number
        elif lastOperator + 1 == i:
            # case like "--1+2" -> ["-", "-", "1", "+", "2"]. the negatives are operators yes, but invalidly applied (not techincally....)
            throwEquationSyntaxErrorWIndex(input_str, errorIdx-1, "Invalid Operator Order")
        else:
            # mark last operator seen
            lastOperator = i

        

    if separatorlevel != 0:
        # invalid parenthesis
        throwEquationSyntaxErrorWIndex(input_str, errorIdx-1,  "Invalid parenthesis level!")

    return output



class Node:
    def __init__(self, value):
        self.value = value

class OperatorNode(Node):
    def __init__(
        self,
        operator : str,
        separatorLevel : int,
        equationPosition : int,
        leftOperand : Node,
    ):
        super().__init__(operator)
        self.operatorPrescendence = operators[operator]["p"]
        self.separatorLevel = separatorLevel
        self.equationPosition = equationPosition
        self.leftOperand = leftOperand
        
    def setRightOperand(self, rightOperand : Node):
        self.rightOperand = rightOperand

    def evaluate(self, op1, op2):
        result = operators[self.value]["f"](op1, op2)
        # print(f"Op: {self.value} {op1=} {op2=} {result=}")
        return result
    
    def hasHigherPrescendence(self, otherOperator : "OperatorNode") -> Optional[bool]:
        """ Return True if has higher prescedence, false if lower"""
        if self.separatorLevel == otherOperator.separatorLevel:
            if self.operatorPrescendence == otherOperator.operatorPrescendence:
                return self.equationPosition < otherOperator.equationPosition
            
            return self.operatorPrescendence > otherOperator.operatorPrescendence
            
        
        return self.separatorLevel > otherOperator.separatorLevel
    
class ValueNode(Node):
    pass


def to_tree(processed_input : list):

    separatorLevel = 0
    root : OperatorNode = None
    lastOperator : OperatorNode = None
    op1 : ValueNode = None
    for i in range(len(processed_input)):
        val = processed_input[i]
        if val in separators:
            if val == openSeparator:
                separatorLevel+=1
            else:
                separatorLevel-=1
            continue

        if val in operators.keys():
            # op1 is guaranteed to be updated before we see an operator
            operator = OperatorNode(val, separatorLevel, i, op1)

            if lastOperator is not None:
                lastOperator.setRightOperand(operator)
            else:
                root = operator

            lastOperator = operator
        else:
            op1 = ValueNode(val)


    # set final operand
    for val in processed_input[::-1]:
        if val not in operators.keys() and val not in separators:
            lastOperator.setRightOperand(ValueNode(val))
            break

    return root

def printroot(node : Node, depth = 0):
    print(f"{" " * (depth+2)}{node.value}", end="")

    if isinstance(node, OperatorNode):
        if isinstance(node.rightOperand, OperatorNode):
            print(f" P: {node.hasHigherPrescendence(node.rightOperand)}")
        else:
            print("")

        printroot(node.leftOperand, depth+1)
        printroot(node.rightOperand, depth+1)

def collapse(node : OperatorNode) -> ValueNode:
    # printroot(node)
    # print("\n\n")
    
    if isinstance(node, OperatorNode):
        if isinstance(node.rightOperand, OperatorNode):
            nextOperator = node.rightOperand
            if node.hasHigherPrescendence(nextOperator):
                # can collapse ourselves ("stealing the right nodes leftoperand")
                NewNode = ValueNode(node.evaluate(node.leftOperand.value, nextOperator.leftOperand.value))
                nextOperator.leftOperand = NewNode

                return collapse(node.rightOperand)
            else:
                # need to collapse bottom first
                node.rightOperand = collapse(node.rightOperand)

        # finally collapse
        return ValueNode(node.evaluate(node.leftOperand.value, node.rightOperand.value))
    
    return node


def repl():
    while True:
        input_str = input("Please enter your equation>>> ").lstrip().rstrip()
        try:
            processed = process_input_str(input_str)
            root = to_tree(processed)
            result = collapse(root)

            print(f"Result: {result.value}")
        except SyntaxError as e:
            print(f"Failed to parse input!: \n{e.__class__.__name__}: {e}")



if __name__ == "__main__":
    repl()