import pytest

from .solution import (
    Stack, process_expression, pre_calc, main_calc, sort_variables)


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
    ('expression', 'values', 'expected'),
    [
        (['a', 2, 2, '+', '*'], {'a': 2}, 8),
        (['a', 2, 2, '+', '*'], {'a': 3}, 12),

        (['a', 'b', '<', 5, 14, '?'], {'a': 10, 'b': 5}, 14),
        (['a', 'b', '<', 5, 14, '?'], {'a': 5, 'b': 10}, 5),

        (['a', 'b', '-'], {'a': 5, 'b': 10}, -5),
        (['a', 'b', '-'], {'a': 10, 'b': 10}, 0),

        (['a', 'b', '/'], {'a': 10, 'b': 10}, 1),
        (['a', 'b', '/'], {'a': 10, 'b': 11}, 0),
        (['a', 'b', '/'], {'a': 10, 'b': 4}, 2),
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
        ([], Stack([4]), {}, 4),
        (['*'], Stack(['a', 4]), {'a': 2}, 8),
    ]
)
def test_process_expression_after_precalc(expression, values, stack, expected):
    assert process_expression(expression, values, stack) == expected


@pytest.mark.parametrize(
    ('expression', 'values_list', 'expected'),
    [
        ('a 2 2 + *'.split(), [{'a': 2}, {'a': 3}], [8, 12]),
        ('a b < 5 14 ?'.split(), [{'a': 10, 'b': 5}, {'a': 5, 'b': 10}], [14, 5]),
    ],
)
def test_main_calc(expression, values_list, expected):
    assert main_calc(expression, values_list) == expected


@pytest.mark.parametrize(
    ('expression', 'expected_values'),
    [
        ('a 2 +'.split(), ['a']),
        ('a b < 5 14 ?'.split(), ['a', 'b']),
        ('a 2 z 80 p - / * +'.split(), ['a', 'p', 'z']),
    ],
)
def test_sort_variables(expression, expected_values):
    assert sort_variables(expression) == expected_values
