from string import ascii_lowercase
from typing import List, Tuple, Dict


class Stack:
    def __init__(self, values=None):
        self._values = values or []

    def push(self, x):
        self._values.append(x)

    def pop(self):
        return self._values.pop()

    def copy(self):
        return type(self)(self._values[:])


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
    if b == 0:
        return 0
    return a // b


def eq(*args):
    b, a = args
    return a == b


def more(*args):
    b, a = args
    return int(a > b)


def less(*args):
    b, a = args
    return int(a < b)


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

LETTERS = set(ascii_lowercase)


def calc(expression: List[str], values: Dict[str, int], stack: Stack):
    """ Calculate given expression with variable values and prepared stack. """
    stack = stack.copy()
    for symbol in expression:
        if isinstance(symbol, int):
            stack.push(symbol)
        elif symbol.isdigit():
            stack.push(int(symbol))
        elif symbol in values:
            stack.push(values[symbol])
        else:
            func, arg_cnt = operation_mapping[symbol]

            args = []
            for _ in range(arg_cnt):
                # at this moment we have only `int` or `variable` on stack
                x = stack.pop()
                if isinstance(x, str):
                    x = values[x]
                args.append(x)
            stack.push(func(*args))
    return stack.pop()


def pre_calc(expression: List[str]) -> Tuple[List[str], Stack]:
    """ Simplify expression before first variable. """
    stack = Stack()
    idx = 0
    for idx, symbol in enumerate(expression):
        if symbol.isdigit():
            stack.push(int(symbol))
        elif symbol in LETTERS:
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


def main_calc(expression: List[str], values_list: List[Dict[str, int]]) -> List[int]:
    pre_expression, pre_stack = pre_calc(expression)
    return [calc(pre_expression, values, pre_stack) for values in values_list]


def convert_values_to_dict(expression: str, value_rows: List[str]) -> List[Dict[str, int]]:
    variables = sorted([x for x in expression.split() if x.isalpha()])
    return [
        {var: int(value) for var, value in zip(variables, value_row.split())}
        for value_row in value_rows
    ]


def read() -> Tuple[str, List[str]]:
    _ = input()
    expression = input()
    cases_cnt = int(input())
    var_values = [input() for _ in range(cases_cnt)]
    return expression, var_values


def main():
    expression, var_values = read()
    values = convert_values_to_dict(expression, var_values)
    for r in main_calc(expression.split(), values):
        print(r)


if __name__ == '__main__':
    main()
