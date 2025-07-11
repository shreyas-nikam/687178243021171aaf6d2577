import pytest
from definition_dea861c4ed46400a8c9fe622090f2c30 import aggregate_firm_risk

@pytest.mark.parametrize("individual_exposures, expected", [
    ([100, 200, 300], 600),
    ([10.5, 20.5, 30.5], 61.5),
    ([10, -5, 5], 10),
    ([0, 0, 0], 0),
    ([], 0)
])
def test_aggregate_firm_risk(individual_exposures, expected):
    assert aggregate_firm_risk(individual_exposures) == expected
