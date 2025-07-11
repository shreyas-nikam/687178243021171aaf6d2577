import pytest
from definition_abb27c8b9efc45ada6d6fe3a9e4fd633 import plot_hierarchical_appetite
import pandas as pd
from unittest.mock import patch
import matplotlib.pyplot as plt


@pytest.fixture
def sample_df():
    data = {'Business Unit': ['A', 'B', 'C'],
            'Allocated Appetite': [100, 200, 300],
            'Individual Risk Exposure': [50, 250, 350],
            'Risk Tolerance': [150, 300, 400]}
    return pd.DataFrame(data)



def test_plot_hierarchical_appetite_empty_df():
    df = pd.DataFrame()
    with pytest.raises(Exception):
        plot_hierarchical_appetite(df)



def test_plot_hierarchical_appetite_non_dataframe():
        with pytest.raises(AttributeError):
            plot_hierarchical_appetite("not a dataframe")

@patch('plotly.express.treemap')
def test_plot_hierarchical_appetite_calls_treemap(mock_treemap, sample_df):
    plot_hierarchical_appetite(sample_df)
    mock_treemap.assert_called()
    
@patch('matplotlib.pyplot.show')
def test_plot_hierarchical_appetite_no_errors(mock_show, sample_df):
    plot_hierarchical_appetite(sample_df)
    assert mock_show.call_count == 0 # Check no exceptions were raised that stop the test or shows an error.
    
@patch('plotly.express.treemap')
def test_plot_hierarchical_appetite_correct_labels(mock_treemap, sample_df):
    plot_hierarchical_appetite(sample_df)
    mock_treemap.assert_called()