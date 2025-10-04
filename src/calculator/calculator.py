from typing import Callable

import numpy as np

from ._trie import Trie
from ._utils import _throwEquationSyntaxErrorWIndex
from ._nodes import Node, ValueNode, ConstantNode, UnaryOpNode, BinaryOpNode
from ._backedlist import BackedList




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


class CalculatorBuilder:
    def __init__(self):
        self.binaryoperators = {}
        self.unaryoperators = {}
        self.constants = {}
        self.suffixoperators = {}

        # default values
        self.negationChar = "-"
        self.openSeparator = "("
        self.closeSeparator = ")"

    def addBinaryOperator(self, symbol : str, precedence : int, func : Callable[[float, float], float]):
        self.binaryoperators[symbol] = {"p": precedence, "f": func}

    def addUnaryOperator(self, symbol : str, func : Callable[[float], float]):
        self.unaryoperators[symbol] = {"f": func}

    def addConstant(self, name : str, value : float):
        self.constants[name] = value

    def addSuffixOperator(self, symbol : str, func : Callable[[float], float]):
        if len(symbol) != 1:
            raise ValueError("Suffix operator symbol must be a single character!")
        self.suffixoperators[symbol] = {"f": func}

    def setNegationChar(self, symbol : str):
        if len(symbol) != 1:
            raise ValueError("Negation character must be a single character!")
        self.negationChar = symbol

    def setSeparators(self, openSep : str, closeSep : str): 
        if len(openSep) != 1 or len(closeSep) != 1:
            raise ValueError("Separators must be a single character!")
        self.openSeparator = openSep
        self.closeSeparator = closeSep

    def build(self) -> "Calculator":
        if len(self.binaryoperators) == 0:
            raise ValueError("Must have at least one binary operator!")

        return Calculator(binaryoperators=self.binaryoperators,
                          unaryoperators=self.unaryoperators,
                          constants=self.constants,
                          suffixoperators=self.suffixoperators,
                          negationChar=self.negationChar,
                          openSeparator=self.openSeparator,
                          closeSeparator=self.closeSeparator)

class Calculator:
    def __init__(self, 
        binaryoperators : dict, 
        unaryoperators : dict, 
        constants : dict, 
        suffixoperators : dict, 
        negationChar : str, 
        openSeparator : str, 
        closeSeparator : str):
        self.binaryoperators = binaryoperators
        self.unaryoperators = unaryoperators
        self.constants = constants
        self.suffixoperators = suffixoperators

        self.negationChar = negationChar
        self.openSeparator = openSeparator
        self.closeSeparator = closeSeparator
        self.separators = {self.openSeparator, self.closeSeparator}

        self.operatorTrie = Trie()

        for op in self.binaryoperators.keys():
            self.operatorTrie.put(op)

        for op in self.unaryoperators.keys():
            self.operatorTrie.put(op)

    def tokenize_input_string(self, input_str : str) -> list[str]:
        input_str = input_str.replace(" ", "")
        backedList = BackedList(input_str)
        lastTokenOperator = False
        operatorbuffer = None

        input_len = len(input_str)
        i = 0

        while i < input_len:
            c = input_str[i]

            # check match against operators
            operatorstr = operatorbuffer + c if operatorbuffer is not None else c
            opmatch = self.operatorTrie.isIn(operatorstr)

            if opmatch == 1:
                # partial match
                operatorbuffer = operatorstr
                i+=1
                continue
            elif opmatch == 2:
                # full match
                if operatorstr in self.unaryoperators.keys():
                    # all unary ops must be wrapped in two separator
                    # op(args)
                    
                    if i > input_len-3:
                        # not enough space for args
                        _throwEquationSyntaxErrorWIndex(input_str, i, "Missing Operator separators!")

                    starti = i
                    i += 1
                    if input_str[i] != self.openSeparator:
                        # should immdiately start with open sep
                        _throwEquationSyntaxErrorWIndex(input_str, i, "Invalid operator separators!")

                    endsep = None

                    i += 1
                    # find next close separator
                    separatorLvl = 1
                    while i < input_len and separatorLvl != 0:
                        next_c = input_str[i]
                        if next_c == self.openSeparator:
                            separatorLvl+=1
                        elif next_c == self.closeSeparator:
                            endsep = i
                            separatorLvl-=1

                        i += 1

                    if separatorLvl != 0:
                        _throwEquationSyntaxErrorWIndex(input_str, i, "Invalid operator separators!")

                    if endsep is None:
                        # not found
                        _throwEquationSyntaxErrorWIndex(input_str, i, "No closing separator!")


                    # slice from [op(args)]
                    startslice = starti-len(operatorstr)+1
                    endslice = endsep+1

                    backedList.addChunk(startslice, starti+1)
                    backedList.addChunk(starti+1, endslice)
                    i = endslice
                    lastTokenOperator = False

                elif operatorstr in self.binaryoperators.keys():
                    # this handles special case of negation, where you might have possibly defined a character for negation, and it might be the same as a binary operator
                    is_special_subtr = operatorstr == self.negationChar and (i == 0 or lastTokenOperator)

                    if not is_special_subtr:
                        backedList.addChunk(i-len(operatorstr)+1, i+1)
                    
                    i += 1

                lastTokenOperator = True
                operatorbuffer = None # reset
                continue

            elif opmatch == 0:
                # no match
                # this means if we had items in the buffer, the addition of the new char c caused it to stop matching
                # try c as its own
                if operatorbuffer is not None:
                    operatorbuffer = None
                    continue
                # else proceed as normal

            # separators are not tokens, just for adjusting order of operations
            if c in self.separators:
                backedList.addChunkI(i)
            else:
                lastTokenOperator = False
                # normal char, part of a number/constant

            i += 1
        
        return backedList.getAsList()        
            

    def validate_and_convert_input_string(self, tokenized_str : list[str], raw_input_str):
        idx_offset = 0
        last_binary_op = -1

        separator_lvl = 0


        i = 0
        while i < len(tokenized_str):
            value = tokenized_str[i]
            idx_offset += len(value)

            is_separator = value in self.separators
            is_binary = value in self.binaryoperators.keys()
            is_unary = value in self.unaryoperators.keys()
            is_expected_numeric = not any([is_separator, is_binary, is_unary])

            if is_separator:
                if value == self.openSeparator:
                    separator_lvl += 1
                else:
                    separator_lvl -= 1

                if separator_lvl < 0:
                    _throwEquationSyntaxErrorWIndex(raw_input_str, idx_offset-1, "Invalid Separators!!")


            elif is_binary:
                if last_binary_op == i-1:
                    _throwEquationSyntaxErrorWIndex(raw_input_str, idx_offset-1, "Multiple Binary Operators in a Row!")

                if i == 0 or i == len(tokenized_str)-1:
                    _throwEquationSyntaxErrorWIndex(raw_input_str, idx_offset-1, "Invalid Binary Operator!")
                

                last_binary_op = i
            elif is_expected_numeric:
                # check if constant
                if value in self.constants.keys():
                    tokenized_str[i] = ConstantNode(self.constants[value])
                # check if some value with a suffix operator: value[suffixoperator]
                elif len(value) > 1 and value[-1:] in self.suffixoperators.keys():
                    func = self.suffixoperators[value[-1:]]

                    #  try conversion to float before applying suffix operator
                    try:
                        value_f = float(value[:-1])
                    except ValueError:
                        _throwEquationSyntaxErrorWIndex(raw_input_str , idx_offset-2, f"Failed to convert: {{{value[:-1]}}} !")
                    
                    tokenized_str[i] = ConstantNode(func(value_f))
                else:
                    #  try conversion to float
                    try:
                        tokenized_str[i] = ConstantNode(float(value))
                    except ValueError:
                        _throwEquationSyntaxErrorWIndex(raw_input_str , idx_offset-1, f"Failed to convert: {{{value}}} !")
            elif is_unary:
                # ops args, are next value
                tokenized_str[i] = UnaryOpNode(value, self.unaryoperators[value]["f"], tokenized_str[i+1], self.calculate)
                # remove the next token, as we are using it immediately
                del tokenized_str[i+1]
            
            i += 1

        if separator_lvl != 0:
            _throwEquationSyntaxErrorWIndex(raw_input_str, idx_offset-1, "Invalid Separator Level!")

        return tokenized_str    
        
    def to_tree(self, processed_input : list):
        separatorLevel = 0
        root : Node = None
        lastBinaryOp : BinaryOpNode = None
        op1 : ValueNode = None

        for i in range(len(processed_input)):
            val = processed_input[i]
            if val in self.separators:
                if val == self.openSeparator:
                    separatorLevel+=1
                else:
                    separatorLevel-=1
                continue

            if type(val) == str and val in self.binaryoperators.keys():
                # op1 is guaranteed to be updated before we see an operator
                operator = BinaryOpNode(val, self.binaryoperators[val]["p"], self.binaryoperators[val]["f"], separatorLevel, i, op1)

                if lastBinaryOp is not None:
                    lastBinaryOp.setRightOperand(operator)
                else:
                    root = operator

                lastBinaryOp = operator
            
            elif issubclass(val.__class__, ValueNode):
                op1 = val
                if root is None:
                    root = val

        # set final operand
        if lastBinaryOp is not None:
            for val in processed_input[::-1]:
                if issubclass(val.__class__, ValueNode):
                    lastBinaryOp.setRightOperand(val)
                    break

        return root
    
    
    def printroot(self, node : Node):
        self._printroot(node)
        print("") # for newline

    def _printroot(self, node : Node, depth = 0):
        print(f"{" " * (depth+2)}{node.getName()}", end="")

        if isinstance(node, BinaryOpNode):
            if isinstance(node.rightOperand, BinaryOpNode):
                print(f" P: {node.hasHigherPrescendence(node.rightOperand)}")
            else:
                print("")

            self._printroot(node.leftOperand, depth+1)
            self._printroot(node.rightOperand, depth+1)

    def collapse(self, node : BinaryOpNode) -> ConstantNode:
        if isinstance(node, BinaryOpNode):
            if isinstance(node.rightOperand, BinaryOpNode):
                nextOperator = node.rightOperand
                if node.hasHigherPrescendence(nextOperator):
                    # can collapse ourselves ("stealing the right nodes leftoperand")
                    NewNode = ConstantNode(node.evaluate(node.leftOperand.getValue(), nextOperator.leftOperand.getValue()))
                    nextOperator.leftOperand = NewNode

                    return self.collapse(node.rightOperand)
                else:
                    # need to collapse bottom first
                    node.rightOperand = self.collapse(node.rightOperand)

            # finally collapse
            return ConstantNode(node.evaluate(node.leftOperand.getValue(), node.rightOperand.getValue()))
        
        if isinstance(node, UnaryOpNode):
            return ConstantNode(node.getValue())
        
        if isinstance(node, ConstantNode):
            return node
        
    def clip_output(self, output : float):
        if np.isclose(output, 0):
            return 0
        if np.isclose(output, np.inf):
            return np.inf
        
        return output

    
    def evaluate_cleaned(self, input_str, debug: bool = False) -> float:
        tokens = self.tokenize_input_string(input_str)
        if debug:
            print(f"{tokens=}")
        processed = self.validate_and_convert_input_string(tokens, input_str)
        if debug:
            print(f"{processed=}")
        tree = self.to_tree(processed)
        if debug:
            self.printroot(tree)
        result = self.clip_output(self.collapse(tree).getValue())
        if debug:
            print(f"{result=}")

        return result

    def calculate(self, raw_input : str, debug: bool = False):
        stripped = raw_input.replace(" ", "")
        
        # remove open/close separators, if nothing is left then error (no actual expression)
        replaced = stripped.replace(self.openSeparator, "").replace(self.closeSeparator, "")

        # no actual expression
        if not replaced:
            raise ValueError("Please enter a valid non-empty expression!")
        else:
            # stripped is now guaranteed to have some actual expression
            return self.evaluate_cleaned(stripped, debug=debug)

