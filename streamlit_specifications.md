
# Streamlit Application Requirements Specification: Risk Appetite & Allocation Modeler

This document outlines the requirements for developing an interactive Streamlit application based on the provided Jupyter Notebook content and user specifications. It serves as a blueprint for implementing the risk appetite and allocation concepts, providing interactive components and relevant code snippets.

## 1. Application Overview

The **Risk Appetite & Allocation Modeler** Streamlit application aims to provide an interactive learning and simulation environment for understanding core concepts of risk appetite, its cascading allocation, and the aggregation of individual risk exposures within an organization. It is designed for risk management practitioners, financial analysts, and business strategy students.

**Objectives:**
*   Enable users to define a firm's top-level `Board Appetite`.
*   Simulate the allocation of this appetite to various business units.
*   Allow input or display of `Individual Risk Exposures` and `Risk Tolerance` for each unit.
*   Visualize the hierarchical breakdown of appetite and the aggregation of risk.
*   Provide a clear comparison of risk exposures against allocated limits using a Red, Amber, Green (RAG) status system.
*   Demonstrate how `Individual Risk Exposures` contribute to the `Total firm risk profile` and its comparison against `Board Appetite`.

## 2. User Interface Requirements

The application will feature an intuitive and interactive user interface, allowing users to manipulate key parameters and instantly observe the impact on risk allocation and status.

### 2.1. Layout and Navigation Structure
*   The application will have a single-page dashboard layout.
*   A clear title: `# Risk Appetite & Allocation Modeler`.
*   An introductory markdown section explaining the purpose, learning outcomes, features, and underlying concepts.
*   Input controls will be organized, possibly in a sidebar or expandable sections, for user-defined parameters.
*   Results and visualizations will be presented in the main content area, following a logical flow.

### 2.2. Input Widgets and Controls
The application will provide interactive widgets for users to define and adjust key parameters:

*   **Board Appetite Definition:**
    *   A `st.slider` or `st.number_input` widget for setting the `Board Appetite` (e.g., in millions of dollars).
    *   **Help Text:** "Set the maximum acceptable annual operational loss for the entire firm."

*   **Cascading Allocation Percentages:**
    *   For each pre-defined business unit (e.g., Retail Banking, Investment Banking, Asset Management, IT Operations), a `st.number_input` widget to specify its `Allocation Percentage`.
    *   **Constraint:** The sum of all allocation percentages must be $100\%$. Live validation will provide feedback if the sum is not $100\%$.
    *   **Help Text:** "Allocate a percentage of the Board Appetite to each business unit. The sum must equal 100%."

*   **Individual Risk Exposure Input (Optional User Override):**
    *   Initially, `Individual Risk Exposures` will be derived from synthetic data.
    *   For each business unit, a `st.number_input` widget will display the synthetic `Individual Risk Exposure`, allowing users to optionally override it with their own values for "what-if" scenarios.
    *   **Help Text:** "View or override the simulated individual risk exposure for each unit (e.g., actual annual losses)."

### 2.3. Visualization Components
The application will leverage interactive charts to present the data effectively. All visuals will adhere to a color-blind-friendly palette and ensure clear titles, labeled axes, and legends.

*   **Summary Table (`st.dataframe`):**
    *   A table displaying for each business unit: `Business Unit`, `Individual_Risk_Exposure`, `Allocated Appetite`, `Absolute Risk Tolerance`, and `Risk Status`.
    *   The `Risk Status` column will be color-coded (Green, Amber, Red).

*   **Comparison Bar Chart:**
    *   A bar chart (using `plotly.express`) comparing `Individual_Risk_Exposure` against `Allocated Appetite` and `Absolute Risk Tolerance` for each business unit.
    *   Bars representing `Individual_Risk_Exposure` will be color-coded based on their `Risk Status` (Green, Amber, Red).
    *   **Title:** "Business Unit Risk Exposure vs. Appetite & Tolerance"
    *   **X-axis:** "Business Unit"
    *   **Y-axis:** "Amount ($)"

*   **Hierarchical Visualization (Treemap or Sunburst Chart):**
    *   A treemap or sunburst chart (using `plotly.express`) visually illustrating:
        *   The `Board Appetite` as the root.
        *   Its breakdown into `Allocated Appetite` for each business unit.
        *   Potentially, `Individual Risk Exposures` aggregated within each allocated segment, with color coding for RAG status.
    *   **Title:** "Hierarchical Risk Appetite Allocation and Exposure"

*   **Overall Firm Risk Profile Summary:**
    *   A clear display of `Total Firm Risk Profile` and `Board Appetite` values.
    *   A conclusive statement indicating whether the `Total Firm Risk Profile` is within or exceeds the `Board Appetite`, along with an interpretation.

### 2.4. Interactive Elements and Feedback Mechanisms
*   All input changes will trigger immediate recalculations and updates to tables and visualizations.
*   Validation errors (e.g., allocation percentages not summing to $100\%$) will be displayed using `st.error` or `st.warning` messages.
*   Tooltips will be provided for all input fields to offer inline help.
*   Color-coding in the bar chart and table will provide quick visual feedback on risk status.

## 3. Additional Requirements

*   **Real-time Updates and Responsiveness:** The Streamlit framework inherently supports real-time updates of the UI upon user interaction with widgets, ensuring a responsive experience.
*   **Annotation and Tooltip Specifications:** As detailed in Section 2.2, all interactive input widgets will include concise `help` text or tooltips to explain their purpose.
*   **Color-Blind-Friendly Palette:** Visualizations will utilize a color palette that is accessible to individuals with color blindness. Standard Plotly Express palettes are generally suitable.
*   **Font Size:** Text and labels within the application and visualizations will maintain a minimum font size of $12 \text{ pt}$ for readability.
*   **Performance:** The application will be designed for efficient computation, ensuring it runs end-to-end in under $5$ minutes on a mid-spec laptop ($8 \text{ GB RAM}$). Synthetic data generation will be kept lightweight.

## 4. Notebook Content and Code Requirements

This section details how the key functions and logic from the Jupyter Notebook will be integrated into the Streamlit application, emphasizing interactive usage.

**4.1. Core Libraries**
The application will import the following Python libraries:
```python
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px # For interactive visualizations
```

**4.2. Synthetic Data Generation**
The `generate_synthetic_data` function will be used to create the baseline dataset for business unit exposures and tolerance factors.

*   **Function Definition (as is from notebook):**
    ```python
    def generate_synthetic_data():
        """Generates a pandas.DataFrame with synthetic data."""
        num_rows = 100 # Can be made a user input via st.slider if desired
        business_units = ['BU_A', 'BU_B', 'BU_C', 'BU_D']
        business_unit_data = np.random.choice(business_units, num_rows)
        individual_risk_exposure_data = np.random.normal(loc=50000, scale=20000, size=num_rows)
        individual_risk_exposure_data = np.abs(individual_risk_exposure_data)
        risk_tolerance_data = np.random.normal(loc=0.7, scale=0.2, size=num_rows)
        risk_tolerance_data = np.clip(risk_tolerance_data, 0.1, 1.0)
        df = pd.DataFrame({
            "Business Unit": business_unit_data,
            "Individual Risk Exposure": individual_risk_exposure_data,
            "Risk Tolerance Factor": risk_tolerance_data
        })
        return df
    ```
*   **Streamlit Integration:**
    *   Call `generate_synthetic_data()` at the start of the Streamlit script (or within a function cached with `@st.cache_data` if `num_rows` is not interactive).
    *   Apply the `bu_mapping` to user-friendly names immediately after generation:
        ```python
        bu_mapping = {
            'BU_A': 'Retail Banking',
            'BU_B': 'Investment Banking',
            'BU_C': 'Asset Management',
            'BU_D': 'IT Operations'
        }
        simulated_data['Business Unit'] = simulated_data['Business Unit'].map(bu_mapping)
        ```
    *   Aggregate `Individual Risk Exposure` and `Risk Tolerance Factor` per business unit.
        ```python
        bu_summary = simulated_data.groupby('Business Unit').agg(
            Individual_Risk_Exposure=('Individual Risk Exposure', 'mean'),
            Risk_Tolerance_Factor=('Risk Tolerance Factor', 'mean')
        ).reset_index()
        # Ensure all expected business units are present in bu_summary
        # (code as in notebook's "3. Aggregate Individual Risk Exposure...")
        ```

**4.3. Validation of Allocation Percentages**
This function ensures that user-provided allocation percentages are valid.

*   **Function Definition (as is from notebook):**
    ```python
    def validate_allocations(percentages):
        """Ensures allocation percentages sum to 100% and are non-negative."""
        epsilon = 1e-6
        total = sum(percentages)
        if not all(p >= 0 for p in percentages):
            raise ValueError("Allocation percentages must be non-negative.")
        if not (100 - epsilon <= total <= 100 + epsilon):
            raise ValueError("Allocation percentages must sum to 100%.")
        return None
    ```
*   **Streamlit Integration:**
    *   Wrap user inputs for allocation percentages in a `try-except` block.
    *   If `validate_allocations` raises a `ValueError`, display the message using `st.error` and prevent further calculations until valid.
    *   This validation should run interactively as the user adjusts percentages.

**4.4. Calculation of Allocated Appetite**
This function implements the core allocation formula.

*   **Formula:**
    $$\text{Allocated Appetite}_i = \text{Board Appetite} \times \frac{\text{Allocation Percentage}_i}{100}$$
*   **Function Definition (as is from notebook):**
    ```python
    def calculate_allocated_appetite(board_appetite, allocation_percentages):
        """Computes the monetary Allocated Appetite for each business unit."""
        return [board_appetite * percentage / 100 for percentage in allocation_percentages]
    ```
*   **Streamlit Integration:**
    *   Call this function using the `board_appetite` from the slider and the validated `allocation_percentages` from user inputs.
    *   The results will populate the `Allocated Appetite` column in the `final_df`.

**4.5. Aggregation of Total Firm Risk Profile**
This function sums up individual exposures to get the overall firm risk.

*   **Formula:**
    $$\text{Total Firm Risk Profile} = \sum_{i=1}^{n} \text{Individual Risk Exposure}_i$$
*   **Function Definition (as is from notebook):**
    ```python
    def aggregate_firm_risk(individual_exposures):
        """Sums individual risk exposures to yield the total firm risk profile."""
        return sum(individual_exposures) if individual_exposures else 0
    ```
*   **Streamlit Integration:**
    *   Call this function on the `Individual_Risk_Exposure` column of the aggregated `final_df`.
    *   Display the result along with the `Board Appetite` and a textual conclusion.

**4.6. Determination of Risk Status (RAG Logic)**
This function applies the Red, Amber, Green (RAG) logic.

*   **Logic:**
    *   If $\text{exposure} \le \text{allocated\_appetite}$, status is 'Green'.
    *   If $\text{allocated\_appetite} < \text{exposure} \le \text{tolerance}$, status is 'Amber'.
    *   If $\text{exposure} > \text{tolerance}$, status is 'Red'.
*   **Function Definition (as is from notebook):**
    ```python
    def determine_risk_status(exposure, allocated_appetite, tolerance):
        """Applies RAG logic to determine risk status."""
        if exposure <= allocated_appetite:
            return 'Green'
        elif exposure <= tolerance: # This implies allocated_appetite < exposure <= tolerance
            return 'Amber'
        else: # This implies tolerance < exposure
            return 'Red'
    ```
*   **Streamlit Integration:**
    *   Apply this function to each row of the `final_df` to compute the `Risk Status` column.
    *   Use this status for color-coding in the table and bar chart.

**4.7. Full Simulation Workflow (Streamlit Orchestration)**

The Streamlit application will orchestrate the above functions in the following sequence:

1.  **Sidebar/Main Area Inputs:**
    *   `Board Appetite` slider/input.
    *   `Allocation Percentages` for each of the `business_units_list`.
        *   On change, trigger `validate_allocations`. If invalid, display error and stop further calculation.
    *   (Optional) `Individual Risk Exposure` overrides for each business unit.

2.  **Data Preparation:**
    *   Call `generate_synthetic_data()` to get initial exposures and tolerance factors.
    *   Map `BU_A` etc. to user-friendly business unit names.
    *   Group and aggregate the synthetic data to get mean `Individual_Risk_Exposure` and `Risk_Tolerance_Factor` per business unit.
    *   Create a `pd.DataFrame` for `allocated_appetites` using `calculate_allocated_appetite`.

3.  **Merge Data:**
    *   Merge the aggregated business unit data with the allocated appetites DataFrame to form `final_df`.
    *   Calculate `Absolute Risk Tolerance` for each business unit:
        $$\text{Absolute Risk Tolerance}_i = \text{Allocated Appetite}_i \times \text{Risk Tolerance Factor}_i$$

4.  **Determine Risk Status:**
    *   Apply `determine_risk_status` to `final_df` to populate the `Risk Status` column.

5.  **Calculate Total Firm Risk:**
    *   Call `aggregate_firm_risk` on the `Individual_Risk_Exposure` column of `final_df`.

6.  **Display Results:**
    *   `st.dataframe(final_df)` displaying the combined data with RAG status.
    *   Plotly Express Bar Chart (`px.bar`) for comparison.
    *   Plotly Express Treemap/Sunburst Chart (`px.treemap` or `px.sunburst`) for hierarchical visualization.
    *   `st.write` or `st.metric` for `Total Firm Risk Profile` and `Board Appetite`, followed by the overall conclusion based on their comparison.

This detailed specification provides the necessary framework and code integration points for developing the interactive Streamlit application.
