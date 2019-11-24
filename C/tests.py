import pytest

from .solution import build_minimum_spanning_tree, convert_graph


@pytest.mark.parametrize(
    ('graph', 'expected_tree'),
    [
        (
            # (1)--10--(2)
            #   \      /
            #   40   20
            #     \ /
            #     (3)
            [
                (10, 1, 2),
                (20, 2, 3),
                (40, 1, 3),
            ],
            # (1)--10--(2)
            #          /
            #        20
            #       /
            #     (3)
            {
                (10, 1, 2),
                (20, 2, 3),
            },
        ),

        (
            # (1)---10--(2)
            #  | \       |
            #  |   \     50
            #  |    20   |
            #  15     \  |
            #  |       \ |
            # (3)--90---(4)
            #   \       /
            #    70   18
            #      \ /
            #      (5)
            [
                (10, 1, 2),
                (20, 1, 4),
                (15, 1, 3),
                (50, 2, 4),
                (90, 4, 3),
                (70, 5, 3),
                (18, 5, 4),
            ],
            # (1)---10--(2)
            #  | \
            #  |   \
            #  |    20
            #  15     \
            #  |       \
            # (3)       (4)
            #           /
            #         18
            #        /
            #      (5)
            {
                (10, 1, 2),
                (20, 1, 4),
                (15, 1, 3),
                (18, 5, 4),
            },
        )
    ]
)
def test_build_minimum_spanning_tree(graph, expected_tree):
    assert build_minimum_spanning_tree(graph) == expected_tree


@pytest.mark.parametrize(
    ('nodes', 'branches', 'expected'),
    [
        (
            {1: 10},
            [],
            {
                (10, -1, 1),
            }
        ),
        (
            {1: 10, 2: 20},
            [],
            {
                (10, -1, 1),
                (20, -1, 2),
            }
        ),
        (
            {1: 10, 2: 20},
            [
                (15, 1, 2),
            ],
            {
                (15, 1, 2),
                (10, -1, 1),
                (20, -1, 2),
            }
        ),
    ]
)
def test_convert_graph(nodes, branches, expected):
    assert convert_graph(nodes, branches) == expected
