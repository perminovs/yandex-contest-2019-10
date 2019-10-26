import pytest

from .solution import (
    Stack, process_expression, get_value, pre_calc, main_calc
)


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
    ('symbol', 'values', 'expected'),
    [
        ('a', [1], 1),
        ('b', [1, 4], 4),
        ('c', [1, 4, 2, -1], 2),
        ('c', [1, 4, 2, -1], 2),
        ('d', [1, 4, 2, -1], -1),
    ]
)
def test_get_value(symbol, values, expected):
    assert get_value(symbol, values) == expected


@pytest.mark.parametrize(
    ('expression', 'values', 'expected'),
    [
        (['a', 2, 2, '+', '*'], [2], 8),
        (['a', 2, 2, '+', '*'], [3], 12),

        (['a', 'b', '<', 5, 14, '?'], [10, 5], 14),
        (['a', 'b', '<', 5, 14, '?'], [5, 10], 5),

        (['a', 'b', '-'], [5, 10], -5),
        (['a', 'b', '-'], [10, 10], 0),

        (['a', 'b', '/'], [10, 10], 1),
        (['a', 'b', '/'], [10, 11], 0),
        (['a', 'b', '/'], [10, 4], 2),
    ]
)
def test_process_expression_without_precalc(expression, values, expected):
    assert process_expression(expression, values, Stack()) == expected


@pytest.mark.parametrize(
    ('expression', 'expected_expression', 'expected_stack'),
    [
        (['2', '2', '+'], [], Stack([4])),
        (['a', '2', '+'], ['+'], Stack(['a', 2])),
        (['a', '2', '2', '+', '*'], ['*'], Stack(['a', 4])),

        (['a', 'b', '<', '5', '14', '?'], ['<', '5', '14', '?'], Stack(['a', 'b'])),
    ]
)
def test_prepare_expression(expression, expected_expression, expected_stack):
    assert pre_calc(expression) == (expected_expression, expected_stack)


@pytest.mark.parametrize(
    ('expression', 'stack', 'values', 'expected'),
    [
        ([], Stack([4]), [4], 4),
        (['*'], Stack(['a', 4]), [2], 8),
    ]
)
def test_process_expression_after_precalc(expression, values, stack, expected):
    assert process_expression(expression, values, stack) == expected


@pytest.mark.parametrize(
    ('expression', 'values_list', 'expected'),
    [
        ('a 2 2 + *'.split(), [[2], [3]], [8, 12]),
        ('a b < 5 14 ?'.split(), [[10, 5], [5, 10]], [14, 5]),
    ],
)
def test_main_calc(expression, values_list, expected):
    assert main_calc(expression, values_list) == expected
