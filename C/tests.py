import pytest

from .graph import build_minimum_spanning_tree


@pytest.mark.parametrize(
    ('graph', 'expected_tree'),
    # (weight, start, end)
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
