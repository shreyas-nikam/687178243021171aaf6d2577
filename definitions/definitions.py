import pandas as pd
import numpy as np

def generate_synthetic_data():
    """Generates a pandas.DataFrame with synthetic data."""

    num_rows = 100  # You can adjust the number of rows as needed

    # Generate synthetic data for Business Unit
    business_units = ['BU_A', 'BU_B', 'BU_C', 'BU_D']
    business_unit_data = np.random.choice(business_units, num_rows)

    # Generate synthetic data for Individual Risk Exposure (numeric)
    individual_risk_exposure_data = np.random.normal(loc=50000, scale=20000, size=num_rows)
    individual_risk_exposure_data = np.abs(individual_risk_exposure_data)  # Ensure positive values

    # Generate synthetic data for Risk Tolerance (numeric)
    risk_tolerance_data = np.random.normal(loc=0.7, scale=0.2, size=num_rows)
    risk_tolerance_data = np.clip(risk_tolerance_data, 0.1, 1.0)  # Ensure values are between 0.1 and 1.0


    # Create the DataFrame
    df = pd.DataFrame({
        "Business Unit": business_unit_data,
        "Individual Risk Exposure": individual_risk_exposure_data,
        "Risk Tolerance": risk_tolerance_data
    })

    return df

def validate_allocations(percentages):
                """Ensures allocation percentages sum to 100% and are non-negative."""
                epsilon = 1e-6
                total = sum(percentages)
                if not all(p >= 0 for p in percentages):
                    raise ValueError("Allocation percentages must be non-negative.")
                if not (100 - epsilon <= total <= 100 + epsilon):
                    raise ValueError("Allocation percentages must sum to 100%.")
                return None

def calculate_allocated_appetite(board_appetite, allocation_percentages):
                """Computes the monetary Allocated Appetite for each business unit.
                """
                return [board_appetite * percentage for percentage in allocation_percentages]

def aggregate_firm_risk(individual_exposures):
    """Sums individual risk exposures to yield the total firm risk profile."""
    return sum(individual_exposures) if individual_exposures else 0

def determine_risk_status(exposure, allocated_appetite, tolerance):
                """Applies RAG logic to determine risk status."""
                if exposure <= allocated_appetite:
                    return 'Green'
                elif exposure <= tolerance:
                    return 'Amber'
                else:
                    return 'Red'