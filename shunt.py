from definitions import OPERATORS, FUNCTIONS, Function
from functools import partial

class Shunt:
    def __init__(self):
        self.output = []
        self.operators = []
        self.args = []
        self.prevOp = True

    # Determines wether the given string is a number, variable, or function,
    # and adds it to the appropriate stack.
    def process(self, string):
        if string == "":
            return
        elif string in FUNCTIONS:
            self.operators.append(FUNCTIONS.get(string))
            self.args.append(1)
        else:
            self.output.append(string)
        self.prevOp = False
    
    # Looks at operators on the top of the stack and transfers them to the output
    # stack if their priority is greater than the given operator, or is equal to
    # and has left associativity. It then appends the given operator to the
    # operators stack.
    def consume(self, operator):
        priority = operator.priority
        while self.operators:
            prev = self.operators[-1]
            if prev == '(':
                break
            elif type(prev) is Function:
                self.output.append(self.operators.pop())
                continue
            prev_priority = prev.priority
            if prev_priority > priority:
                self.output.append(self.operators.pop())
            elif prev_priority == priority and prev.associativity == "Left":
                self.output.append(self.operators.pop())
            else:
                break
        self.operators.append(operator)

    def consume_until_bracket(self):
        while self.operators:
            prev = self.operators[-1]
            if prev == '(':
                break
            else:
                self.output.append(self.operators.pop())

    # Pops operators from the operators stack and appends them to the output until
    # a left bracket ')' is found. If no bracket is found, a SyntaxError is raised.
    # If the operator before the bracket is a function, it is also appended.
    def match_bracket(self):
        while True:
            if self.operators:
                operator = self.operators.pop()
                if operator == '(':
                    break
                else:
                    self.output.append(operator)
            else:
                raise SyntaxError("Incorrect number of brackets")
        if self.operators:
            operator = self.operators[-1]
            if type(operator) is Function:
                function = self.operators.pop()
                function.args = self.args.pop()
                self.output.append(function)


    # Takes an infix notation expression and converts it to postfix.
    def convert(self, string):
        current = ""
        for char in string:
            if char in OPERATORS:
                self.process(current)
                current = ""
                if self.prevOp:
                    self.process(char)
                else:
                    self.consume(OPERATORS.get(char))
                self.prevOp = True
            elif char == ',':
                self.process(current)
                self.consume_until_bracket()
                self.args[-1] += 1
                current = ""
            elif char == '(':
                self.process(current)
                current = ""
                self.operators.append('(')
            elif char == ')':
                self.process(current)
                current = ""
                self.match_bracket()
            elif char == ' ':
                continue
            else:
                current = current + char
        self.process(current)
        self.output.extend(reversed(self.operators))
        return self.output        