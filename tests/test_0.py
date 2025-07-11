import pytest
import pandas as pd
from definition_d63106a6bc90458cbb1d395e5ad0dbd5 import generate_synthetic_data

def test_generate_synthetic_data_returns_dataframe():
    df = generate_synthetic_data()
    assert isinstance(df, pd.DataFrame)

def test_generate_synthetic_data_has_expected_columns():
    df = generate_synthetic_data()
    expected_columns = ["Business Unit", "Individual Risk Exposure", "Risk Tolerance"]
    assert all(col in df.columns for col in expected_columns)

def test_generate_synthetic_data_numeric_columns_are_numeric():
    df = generate_synthetic_data()
    assert pd.api.types.is_numeric_dtype(df["Individual Risk Exposure"])
    assert pd.api.types.is_numeric_dtype(df["Risk Tolerance"])

def test_generate_synthetic_data_no_missing_values_in_critical_columns():
    df = generate_synthetic_data()
    assert df["Business Unit"].isnull().sum() == 0
    assert df["Individual Risk Exposure"].isnull().sum() == 0
    assert df["Risk Tolerance"].isnull().sum() == 0

def test_generate_synthetic_data_returns_non_empty_dataframe():
    df = generate_synthetic_data()
    assert not df.empty
