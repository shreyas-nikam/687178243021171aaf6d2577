import pytest
from definition_4113b4f440fa4311a26b3a903a3b6c82 import calculate_allocated_appetite

@pytest.mark.parametrize("board_appetite, allocation_percentages, expected", [
    (100.0, [0.2, 0.3, 0.5], [20.0, 30.0, 50.0]),
    (50.0, [0.1, 0.4, 0.5], [5.0, 20.0, 25.0]),
    (200.0, [0.0, 0.0, 1.0], [0.0, 0.0, 200.0]),
    (100.0, [0.25, 0.25, 0.25, 0.25], [25.0, 25.0, 25.0, 25.0]),
    (0.0, [0.3, 0.4, 0.3], [0.0, 0.0, 0.0]),
])
def test_calculate_allocated_appetite(board_appetite, allocation_percentages, expected):
    assert calculate_allocated_appetite(board_appetite, allocation_percentages) == expected
