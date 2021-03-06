from definitions import Operator, Function, CONSTANTS
from number import Number
from shunt import Shunt

def rpn(output, variables, file, samples):
    stack = []
    for element in output:
        if type(element) is Operator:
            num2 = stack.pop()
            num1 = stack.pop()
            evaluated = element.function(num1, num2)
            if samples:
                file.write(evaluated.getError() + "\n")
            stack.append(evaluated)
        elif type(element) is Function:
            count = 0
            args = []
            while count < element.args:
                args.append(stack.pop())
                count += 1
            if len(args) == 1:
                args = args[0]
            evaluated = element.function(args)
            if samples:
                file.write(evaluated.getError() + "\n")
            stack.append(evaluated)
        else:
            if element in variables:
                stack.append(variables.get(element))
            elif element in CONSTANTS:
                stack.append(CONSTANTS.get(element))
            else:
                number = Number(float(element), element)
                stack.append(number)
    return stack.pop()