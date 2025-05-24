from trie import Trie
from backedlist import BackedList
from operators import binaryoperators, unaryoperators, separators, openSeparator, closeSeparator, negationChar, constants
from nodes import BinaryOpNode, UnaryOpNode, ConstantNode, ValueNode, Node

operatorTrie = Trie()

for op in unaryoperators.keys():
    operatorTrie.put(op)

for op in binaryoperators.keys():
    operatorTrie.put(op)




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

class Calculator:
    def __init__(self):
        pass

    def __throwEquationSyntaxErrorWIndex(self, equation_input : str,  index : int, errorDescription : str = "error here"):
        raise SyntaxError(f"{equation_input} is not a valid equation!\n"+
                          f"{len(SyntaxError.__name__ + ": ") * " "}{"~"*index}^ {errorDescription}")

    def tokenize_input_string(self, input_str : str) -> list[str]:
        input_str = input_str.replace(" ", "")
        backedList = BackedList(input_str)
        lastOperatorIdx = -1
        operatorbuffer = None

        input_len = len(input_str)
        i = 0

        while i < input_len:
            c = input_str[i]

            # check match against operators
            operatorstr = operatorbuffer + c if operatorbuffer is not None else c
            opmatch = operatorTrie.isIn(operatorstr)

            if opmatch == 1:
                # partial match
                operatorbuffer = operatorstr
                i+=1
                continue
            elif opmatch == 2:
                # full match
                if operatorstr in unaryoperators.keys():
                    # all unary ops must be wrapped in two separator
                    # op(args)
                    startsep = input_str.find(openSeparator, i)
                    endsep = input_str.find(closeSeparator, i+2) # skip expected opening separator, and at least one char of input

                    if startsep == -1 or endsep == -1:
                        self.__throwEquationSyntaxErrorWIndex(input_str, i, "Invalid operator separators!")

                    # slice from [op(args)]
                    startslice = i-len(operatorstr)+1
                    endslice = endsep+1

                    backedList.addChunk(startslice, i+1)
                    backedList.addChunk(i+1, endslice)
                    i = endslice

                elif operatorstr in binaryoperators.keys():
                    # binary op can be independednt
                    is_special_subtr = operatorstr == negationChar and (i == 0 or lastOperatorIdx == i-1)

                    if not is_special_subtr:
                        backedList.addChunk(i-len(operatorstr)+1, i+1)
                    
                    i += 1

                lastOperatorIdx = i-1 # due to custom incrementation
                operatorbuffer = None # reset
                continue

            if c in separators:
                backedList.addChunkI(i)


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

            is_separator = value in separators
            is_binary = value in binaryoperators.keys()
            is_unary = value in unaryoperators.keys()
            is_expected_numeric = not any([is_separator, is_binary, is_unary])

            if is_separator:
                if value == openSeparator:
                    separator_lvl += 1
                else:
                    separator_lvl -= 1

            elif is_binary:
                if last_binary_op == i-1:
                    self.__throwEquationSyntaxErrorWIndex(raw_input_str, idx_offset-1, "Multiple Binary Operators in a Row!")

                if i == 0 or i == len(tokenized_str)-1:
                    self.__throwEquationSyntaxErrorWIndex(raw_input_str, idx_offset-1, "Invalid Binary Operator!")
                

                last_binary_op = i
            elif is_expected_numeric:
                # check if constant
                if value in constants.keys():
                    tokenized_str[i] = ConstantNode(constants[value])
                else:
                    #  try conversion to float
                    try:
                        tokenized_str[i] = ConstantNode(float(value))
                    except ValueError:
                        self.__throwEquationSyntaxErrorWIndex(raw_input_str , idx_offset-1, f"Failed to convert: {value}!")
            elif is_unary:
                # ops args, are next value
                tokenized_str[i] = UnaryOpNode(value, tokenized_str[i+1], self.evaluate)
                # remove the next token
                del tokenized_str[i+1]
            
            i += 1

        if separator_lvl != 0:
            self.__throwEquationSyntaxErrorWIndex(raw_input_str, idx_offset-1, "Invalid Separator Level!")

        return tokenized_str    
        
    def to_tree(self, processed_input : list):
        separatorLevel = 0
        root : Node = None
        lastBinaryOp : BinaryOpNode = None
        op1 : ValueNode = None

        for i in range(len(processed_input)):
            val = processed_input[i]
            if val in separators:
                if val == openSeparator:
                    separatorLevel+=1
                else:
                    separatorLevel-=1
                continue

            if type(val) == str and val in binaryoperators.keys():
                # op1 is guaranteed to be updated before we see an operator
                operator = BinaryOpNode(val, separatorLevel, i, op1)

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
    
    def evaluate(self, input_str, debug: bool = True) -> ConstantNode:
        tokens = self.tokenize_input_string(input_str)
        if debug:
            print(f"{tokens=}")
        processed = self.validate_and_convert_input_string(tokens, input_str)
        if debug:
            print(f"{processed=}")
        tree = self.to_tree(processed)
        if debug:
            self.printroot(tree)
        result = self.collapse(tree)
        print(f"{result.getValue()=}")

        return result


def repl():
    c = Calculator()

    while True:
        input_str = input("Please enter your equation>>> ")
        try:
            result = c.evaluate(input_str).getValue()
            print(f"Result: {result}")

        except SyntaxError as e:
            print(f"Failed to parse input!: \n{e.__class__.__name__}: {e}")



if __name__ == "__main__":
    repl()