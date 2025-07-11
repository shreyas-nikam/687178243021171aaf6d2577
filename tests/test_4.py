import pytest
from definition_b2b5e6b74d61451193d7f4531d8012c5 import determine_risk_status

@pytest.mark.parametrize("exposure, allocated_appetite, tolerance, expected", [
    (50, 100, 150, 'Green'),  # Exposure within appetite
    (120, 100, 150, 'Amber'), # Exposure exceeds appetite, within tolerance
    (160, 100, 150, 'Red'),   # Exposure exceeds tolerance
    (100, 100, 100, 'Green'), # Exposure equals appetite and tolerance
    (0, 100, 150, 'Green'),    # Zero exposure
])
def test_determine_risk_status(exposure, allocated_appetite, tolerance, expected):
    assert determine_risk_status(exposure, allocated_appetite, tolerance) == expected
