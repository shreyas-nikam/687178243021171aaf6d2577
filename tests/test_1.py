import pytest
from definition_2a419db450a14ea0af502a6c56658e40 import validate_allocations

@pytest.mark.parametrize("percentages, expected", [
    ([25, 25, 25, 25], True),
    ([0, 0, 0, 0], False),
    ([100], True),
    ([50, 50.0000001], True),
    ([-10, 110], False),
])
def test_validate_allocations(percentages, expected):
    if expected is True:
        assert validate_allocations(percentages) is None
    else:
        with pytest.raises(ValueError):
            validate_allocations(percentages)
