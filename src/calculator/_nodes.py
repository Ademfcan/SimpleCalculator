from typing import Callable


class Node:
    def __init__(self, name : str):
        self.name = name

    def getName(self):
        return self.name
    
class ValueNode(Node):
    def getValue(self):
        pass

class ConstantNode(ValueNode):
    def __init__(self, value):
        super().__init__(value)
        self.value = value
    
    def getValue(self):
        return self.value
    
class UnaryOpNode(ValueNode):
    def __init__(self, operator : str, operatorFunc : Callable[[float], float], argument_wparen : str, recursive_evaluate_func : Callable[[str], float]):
        super().__init__(f"{operator}{argument_wparen}")
        self.operator = operator
        self.func = operatorFunc
        self.recursive_evaluate_func = recursive_evaluate_func
        self.argument = argument_wparen[1:-1]

    def getValue(self):
        # the recursive evaluate func handles equations inside the argument, eg sin(1+1) or sin(cos(1))
        return self.func(self.recursive_evaluate_func(self.argument))
    

class BinaryOpNode(Node):
    def __init__(
        self,
        operator : str,
        operatorPrescendence : int,
        operatorFunc: Callable[[float, float], float],
        separatorLevel : int,
        equationPosition : int,
        leftOperand : ValueNode,
    ):
        super().__init__(operator)
        self.operatorPrescendence = operatorPrescendence
        self.separatorLevel = separatorLevel
        self.func = operatorFunc

        self.equationPosition = equationPosition
        self.leftOperand = leftOperand
        
    def setRightOperand(self, rightOperand : Node):
        self.rightOperand = rightOperand

    def evaluate(self, op1, op2):
        result = self.func(op1, op2)
        # print(f"Op: {self.value} {op1=} {op2=} {result=}")
        return result
    
    def hasHigherPrescendence(self, otherOperator : "BinaryOpNode") -> bool:
        """ Return True if has higher prescedence, false if lower"""
        if self.separatorLevel == otherOperator.separatorLevel:
            if self.operatorPrescendence == otherOperator.operatorPrescendence:
                return self.equationPosition < otherOperator.equationPosition
            
            return self.operatorPrescendence > otherOperator.operatorPrescendence
            
        
        return self.separatorLevel > otherOperator.separatorLevel
    