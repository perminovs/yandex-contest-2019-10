from string import ascii_lowercase
from typing import List, Tuple


class Stack:
    def __init__(self, values=None):
        self._values = values or []

    def push(self, x):
        self._values.append(x)

    def pop(self):
        return self._values.pop()

    def copy(self):
        return type(self)(self._values[:])

    def __repr__(self):
        return repr(self._values)

    def __eq__(self, other):
        return self._values == other._values


def plus(*args):
    b, a = args
    return a + b


def minus(*args):
    b, a = args
    return a - b


def multiply(*args):
    b, a = args
    return a * b


def divide(*args):
    b, a = args
    return a // b


def eq(*args):
    b, a = args
    return a == b


def more(*args):
    b, a = args
    return a > b


def less(*args):
    b, a = args
    return a < b


def choose(*args):
    b, a, cond = args
    return a if cond else b


operation_mapping = {
    '+': (plus, 2),
    '-': (minus, 2),
    '*': (multiply, 2),
    '/': (divide, 2),
    '<': (less, 2),
    '>': (more, 2),
    '=': (eq, 2),
    '?': (choose, 3),
}

letters = {let: number for number, let in enumerate(ascii_lowercase)}


def get_value(symbol, values):
    idx = letters[symbol]
    return values[idx]


def process_expression(expression: List[str], values: List[int], stack: Stack):
    stack = stack.copy()
    for symbol in expression:
        if isinstance(symbol, int):
            stack.push(symbol)
        elif symbol.isdigit():
            stack.push(int(symbol))
        elif symbol in letters:
            stack.push(get_value(symbol, values))
        else:
            func, arg_cnt = operation_mapping[symbol]

            args = []
            for _ in range(arg_cnt):
                # at this moment we have only `int` or `variable` on stack
                x = stack.pop()
                if isinstance(x, str):
                    x = get_value(x, values)
                args.append(x)
            stack.push(func(*args))
    return stack.pop()


def pre_calc(expression: List[str]) -> Tuple[List[str], Stack]:
    stack = Stack()
    idx = 0
    for idx, symbol in enumerate(expression):
        if symbol.isdigit():
            stack.push(int(symbol))
        elif symbol in letters:
            stack.push(symbol)
        else:
            func, arg_cnt = operation_mapping[symbol]
            args = [stack.pop() for _ in range(arg_cnt)]
            if any((isinstance(x, str)) for x in args):
                # cannot process expression because it has variable,
                # return values back to stack
                for x in reversed(args):
                    stack.push(x)

                # operation hasn't been processed yet,
                # we should place it back to expression list
                idx -= 1
                break
            stack.push(func(*args))

    return expression[idx + 1:], stack


def main_calc(expression: List[str], values_list: List[List[int]]) -> List[int]:
    pre_expression, pre_stack = pre_calc(expression)
    return [
        process_expression(pre_expression, values, pre_stack)
        for values in values_list
    ]
