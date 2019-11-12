import pytest

from .solution import Stack, main_calc, convert_values_to_dict


Stack.__repr__ = lambda self: repr(self._values)
Stack.__eq__ = lambda self, other: self._values == other._values


@pytest.fixture(params=[[]])
def stack_initial_values(request):
    return request.param


@pytest.fixture()
def stack(stack_initial_values):
    return Stack(stack_initial_values[:])


def test_push(stack):
    x = 1
    stack.push(x)
    assert stack.pop() == x


@pytest.mark.parametrize(
    'stack_initial_values',
    [[1], [2, 48], [0, 2, 3]],
    indirect=True,
)
def test_pop(stack, stack_initial_values):
    assert stack.pop() == stack_initial_values[-1]


def test_error_on_empty_pop(stack):
    with pytest.raises(IndexError):
        stack.pop()


@pytest.mark.parametrize(
    ('expression', 'values_list', 'expected'),
    [
        ('a 2 2 + *'.split(), [{'a': 2}, {'a': 3}], [8, 12]),
        ('2 a 3 4 + * +'.split(), [{'a': 1}], [9]),
        ('2 a 3 4 + * + 1 +'.split(), [{'a': 1}], [10]),
        ('2 a 3 4 + * + 1 + b +'.split(), [{'a': 1, 'b': 3}], [13]),
        ('a b < 5 14 ?'.split(), [{'a': 10, 'b': 5}, {'a': 5, 'b': 10}], [14, 5]),
        ('0 a a 0 0 + + + +'.split(), [{'a': 10}, {'a': 5}], [20, 10]),
        ('0 a a 0 0 + + + +'.split(), [{'a': 10}, {'a': 5}], [20, 10]),
    ],
)
def test_main_calc(expression, values_list, expected):
    assert main_calc(expression, values_list) == expected


@pytest.mark.parametrize(
    ('expression', 'value_rows', 'expected_dict'),
    [
        ('a 2 +', ['2', '3'], [{'a': 2}, {'a': 3}]),
        ('a b < 5 14 ?', ['5 10', '10 5'], [{'a': 5, 'b': 10}, {'a': 10, 'b': 5}]),
        ('a 2 w 80 p - / * +', ['1 2 3'], [{'a': 1, 'p': 2, 'w': 3}]),
        ('a a 2 w 80 p - - / * +', ['1 2 3'], [{'a': 1, 'p': 2, 'w': 3}]),
    ],
)
def test_read_values(expression, value_rows, expected_dict):
    assert convert_values_to_dict(expression, value_rows) == expected_dict
