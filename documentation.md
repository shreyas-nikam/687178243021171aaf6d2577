id: 687178243021171aaf6d2577_documentation
summary: Second lab of Module 4 Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: A Comprehensive Guide to Risk Appetite & Allocation Modeling with Streamlit

## 1. Introduction to Risk Appetite and QuLab
Duration: 0:05:00

In the dynamic world of finance and business, effectively managing risk is paramount for an organization's sustained success. A crucial component of robust risk management is defining and adhering to a **Risk Appetite**. Risk appetite represents the maximum level of risk a firm is willing to accept in pursuit of its strategic objectives. Without a clear risk appetite, an organization might unknowingly take on excessive risks, potentially leading to financial instability or failure to achieve its goals.

This codelab introduces **QuLab**, a Streamlit-powered interactive application designed to demystify the concepts of risk appetite, its hierarchical allocation, and the real-time assessment of risk exposures. It provides a practical framework for understanding how top-level firm-wide risk appetite translates into actionable limits for individual business units.

### Key Concepts Explored:

*   **Board Appetite:** The overarching maximum risk tolerance set by the firm's leadership. This is the firm's strategic risk boundary.
*   **Allocated Appetite:** The portion of the Board Appetite that is distributed to specific business units or departments. This ensures each unit operates within defined risk limits aligned with the overall firm strategy.
*   **Individual Risk Exposure:** The actual or estimated risk faced by a particular business unit. This could be operational losses, market risk, credit risk, etc.
*   **Risk Tolerance:** The acceptable deviation from the allocated appetite before management action is triggered. It is often expressed as a factor that, when multiplied by Allocated Appetite, yields the `Absolute Risk Tolerance`.
*   **Risk Status (RAG - Red, Amber, Green):** A visual indicator system to quickly assess a business unit's risk posture:
    *   `Green`: Individual Risk Exposure $\le$ Allocated Appetite. The unit is operating comfortably within its allocated limits.
    *   `Amber`: Allocated Appetite $<$ Individual Risk Exposure $\le$ Absolute Risk Tolerance. The unit is exceeding its appetite but is still within an acceptable tolerance zone, requiring monitoring or minor action.
    *   `Red`: Individual Risk Exposure $>$ Absolute Risk Tolerance. The unit's risk exposure significantly exceeds its tolerance, necessitating immediate management intervention.

This codelab will guide you through setting up, understanding, and interacting with the QuLab application. You will learn how the application:
*   Allows defining a firm's `Board Appetite`.
*   Facilitates the cascading allocation of this appetite to various business units.
*   Visualizes individual business unit risk exposures against their allocated limits.
*   Aggregates individual risk exposures to form the `Total Firm Risk Profile`.
*   Compares the `Total Firm Risk Profile` with the `Board Appetite` to provide a holistic assessment of the firm's risk health.

By the end of this codelab, you will have a clear understanding of the architectural flow and the underlying logic of a practical risk appetite framework.

The application is structured into three Python files:
*   `app.py`: The main Streamlit entry point, handling navigation and overall layout.
*   `application_pages/page1.py`: Contains the core `Risk Appetite Modeler` logic and visualizations.
*   `application_pages/page2.py` and `application_pages/page3.py`: Placeholder pages for future enhancements and static resources.

## 2. Setting up the Environment
Duration: 0:03:00

To run the QuLab application, you'll need Python installed on your system, along with a few libraries.

### Prerequisites

*   Python 3.8+

### 2.1. Create a Project Directory

First, create a new directory for your project and navigate into it:

```bash
mkdir QuLab_Codelab
cd QuLab_Codelab
```

### 2.2. Create a Virtual Environment (Recommended)

It's good practice to use a virtual environment to manage dependencies:

```bash
python -m venv venv
```

Activate the virtual environment:

*   On Windows:
    ```bash
    .\venv\Scripts\activate
    ```
*   On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

### 2.3. Install Dependencies

Install the necessary Python libraries using pip:

```bash
pip install streamlit pandas numpy plotly
```

### 2.4. Create Application Files

Now, create the Python files for the application.

First, create the `application_pages` directory:

```bash
mkdir application_pages
```

Then, create the following files with the content provided:

**`app.py`**
```python
import streamlit as st

st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()
st.markdown("""
In this lab, we explore the core concepts of **Risk Appetite & Allocation** within an organizational context.
This interactive application allows you to:
- Define a firm's top-level `Board Appetite`.
- Simulate the cascading allocation of this appetite to various business units.
- Visualize individual business unit risk exposures against their allocated limits.
- Understand how individual risk exposures aggregate to form the `Total Firm Risk Profile`.
- Compare the `Total Firm Risk Profile` with the `Board Appetite` to assess overall firm health.

### Key Concepts:
- **Board Appetite:** The maximum level of risk a firm is willing to accept to achieve its strategic objectives.
- **Allocated Appetite:** The portion of the Board Appetite assigned to specific business units or functions.
- **Individual Risk Exposure:** The actual or estimated risk a specific business unit is facing (e.g., operational losses).
- **Risk Tolerance:** The acceptable deviation from the allocated appetite before triggering management action. It is expressed as a factor that, when multiplied by Allocated Appetite, gives Absolute Risk Tolerance.
- **Risk Status (RAG):**
    - `Green`: Exposure $\le$ Allocated Appetite
    - `Amber`: Allocated Appetite $<$ Exposure $\le$ Absolute Risk Tolerance
    - `Red`: Exposure $>$ Absolute Risk Tolerance

This model helps in understanding the hierarchical breakdown of risk appetite and the aggregation of risk exposures, providing a visual comparison of risk against limits using a Red, Amber, Green (RAG) status system.
""")

page = st.sidebar.selectbox(label="Navigation", options=["Risk Appetite Modeler", "Page 2", "Page 3"])

if page == "Risk Appetite Modeler":
    from application_pages.page1 import run_page1
    run_page1()
elif page == "Page 2":
    from application_pages.page2 import run_page2
    run_page2()
elif page == "Page 3":
    from application_pages.page3 import run_page3
    run_page3()
```

**`application_pages/page1.py`**
```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 4.2. Synthetic Data Generation
@st.cache_data
def generate_synthetic_data():
    """Generates a pandas.DataFrame with synthetic data."""
    num_rows = 100
    business_units = ['BU_A', 'BU_B', 'BU_C', 'BU_D']
    business_unit_data = np.random.choice(business_units, num_rows)
    individual_risk_exposure_data = np.random.normal(loc=50000, scale=20000, size=num_rows)
    individual_risk_exposure_data = np.abs(individual_risk_exposure_data)
    risk_tolerance_data = np.random.normal(loc=0.7, scale=0.2, size=num_rows)
    risk_tolerance_data = np.clip(risk_tolerance_data, 0.1, 1.0) # Ensure tolerance is between 0.1 and 1.0
    df = pd.DataFrame({
        "Business Unit": business_unit_data,
        "Individual Risk Exposure": individual_risk_exposure_data,
        "Risk Tolerance Factor": risk_tolerance_data
    })
    return df

# 4.3. Validation of Allocation Percentages
def validate_allocations(percentages):
    """Ensures allocation percentages sum to 100% and are non-negative."""
    epsilon = 1e-6
    total = sum(percentages)
    if not all(p >= 0 for p in percentages):
        raise ValueError("Allocation percentages must be non-negative.")
    if not (100 - epsilon <= total <= 100 + epsilon):
        raise ValueError("Allocation percentages must sum to 100%.")
    return None

# 4.4. Calculation of Allocated Appetite
def calculate_allocated_appetite(board_appetite, allocation_percentages):
    """Computes the monetary Allocated Appetite for each business unit."""
    return [board_appetite * percentage / 100 for percentage in allocation_percentages]

# 4.5. Aggregation of Total Firm Risk Profile
def aggregate_firm_risk(individual_exposures):
    """Sums individual risk exposures to yield the total firm risk profile."""
    return sum(individual_exposures) if individual_exposures.any() else 0 # Use .any() for pandas Series

# 4.6. Determination of Risk Status (RAG Logic)
def determine_risk_status(exposure, allocated_appetite, tolerance):
    """Applies RAG logic to determine risk status."""
    if exposure <= allocated_appetite:
        return 'Green'
    elif exposure <= tolerance: # This implies allocated_appetite < exposure <= tolerance
        return 'Amber'
    else: # This implies tolerance < exposure
        return 'Red'

def run_page1():
    st.header("Risk Appetite & Allocation Modeler")

    # Business Units Definition
    business_units_list = ['Retail Banking', 'Investment Banking', 'Asset Management', 'IT Operations']

    # 1. Sidebar/Main Area Inputs
    st.subheader("Define Parameters")
    col1, col2 = st.columns(2)

    with col1:
        board_appetite = st.slider(
            "Board Appetite ($ Millions)",
            min_value=100_000,
            max_value=10_000_000,
            value=2_000_000,
            step=100_000,
            help="Set the maximum acceptable annual operational loss for the entire firm."
        )

    with col2:
        st.markdown("##### Allocation Percentages (%)")
        allocation_percentages_input = {}
        for bu in business_units_list:
            allocation_percentages_input[bu] = st.number_input(
                f"Allocate to {bu}",
                min_value=0.0,
                max_value=100.0,
                value=float(100/len(business_units_list)),
                step=0.1,
                help="Allocate a percentage of the Board Appetite to each business unit. The sum must equal 100%."
            )
        current_sum = sum(allocation_percentages_input.values())
        st.info(f"Current sum of allocations: {current_sum:.1f}%")

        try:
            validate_allocations(list(allocation_percentages_input.values()))
            allocation_percentages_valid = True
            st.success("Allocation percentages sum to 100%!")
        except ValueError as e:
            allocation_percentages_valid = False
            st.error(f"Validation Error: {e}")

    if not allocation_percentages_valid:
        st.warning("Please correct allocation percentages to proceed with calculations.")
        return # Stop execution if allocations are invalid

    # 2. Data Preparation
    simulated_data = generate_synthetic_data()

    bu_mapping = {
        'BU_A': 'Retail Banking',
        'BU_B': 'Investment Banking',
        'BU_C': 'Asset Management',
        'BU_D': 'IT Operations'
    }
    simulated_data['Business Unit'] = simulated_data['Business Unit'].map(bu_mapping)

    # Aggregate Individual Risk Exposure and Risk Tolerance Factor per business unit
    bu_summary = simulated_data.groupby('Business Unit').agg(
        Individual_Risk_Exposure=('Individual Risk Exposure', 'mean'),
        Risk_Tolerance_Factor=('Risk Tolerance Factor', 'mean')
    ).reset_index()

    # Ensure all expected business units are present in bu_summary
    # (This ensures consistent display even if synthetic data doesn't generate all BUs)
    missing_bus = [bu for bu in business_units_list if bu not in bu_summary['Business Unit'].values]
    if missing_bus:
        missing_df = pd.DataFrame({
            "Business Unit": missing_bus,
            "Individual_Risk_Exposure": [0.0] * len(missing_bus), # Default to 0 for missing
            "Risk_Tolerance_Factor": [0.7] * len(missing_bus) # Default tolerance
        })
        bu_summary = pd.concat([bu_summary, missing_df], ignore_index=True)

    # Sort to maintain consistent order
    bu_summary['Business Unit'] = pd.Categorical(bu_summary['Business Unit'], categories=business_units_list, ordered=True)
    bu_summary = bu_summary.sort_values('Business Unit').reset_index(drop=True)


    st.subheader("Individual Risk Exposure Overrides (Optional)")
    st.markdown("View or override the simulated individual risk exposure for each unit (e.g., actual annual losses).")
    user_overrides = {}
    for idx, bu in enumerate(business_units_list):
        default_exposure = bu_summary.loc[bu_summary['Business Unit'] == bu, 'Individual_Risk_Exposure'].iloc[0]
        user_overrides[bu] = st.number_input(
            f"Override Exposure for {bu}",
            min_value=0.0,
            value=float(default_exposure),
            step=1000.0,
            key=f"exposure_{bu}"
        )
    # Apply overrides
    for bu, override_val in user_overrides.items():
        bu_summary.loc[bu_summary['Business Unit'] == bu, 'Individual_Risk_Exposure'] = override_val


    # Calculate Allocated Appetite
    allocated_appetites_values = calculate_allocated_appetite(
        board_appetite,
        [allocation_percentages_input[bu] for bu in business_units_list]
    )
    allocated_appetites_df = pd.DataFrame({
        "Business Unit": business_units_list,
        "Allocated Appetite": allocated_appetites_values
    })

    # 3. Merge Data
    final_df = pd.merge(bu_summary, allocated_appetites_df, on="Business Unit")

    # Calculate Absolute Risk Tolerance
    final_df['Absolute Risk Tolerance'] = final_df['Allocated Appetite'] * final_df['Risk_Tolerance_Factor']

    # 4. Determine Risk Status
    final_df['Risk Status'] = final_df.apply(
        lambda row: determine_risk_status(
            row['Individual_Risk_Exposure'],
            row['Allocated Appetite'],
            row['Absolute Risk Tolerance']
        ),
        axis=1
    )

    # 5. Calculate Total Firm Risk
    total_firm_risk = aggregate_firm_risk(final_df['Individual_Risk_Exposure'])

    st.divider()
    st.subheader("Summary of Risk Allocation & Status")

    # 2.3. Visualization Components - Summary Table
    # Define color mapping for RAG status in the table
    def color_status(val):
        if val == 'Green':
            return 'background-color: #d4edda; color: #155724' # Light green, dark green text
        elif val == 'Amber':
            return 'background-color: #fff3cd; color: #856404' # Light yellow, dark yellow text
        elif val == 'Red':
            return 'background-color: #f8d7da; color: #721c24' # Light red, dark red text
        return ''

    styled_df = final_df.style.applymap(color_status, subset=['Risk Status'])
    st.dataframe(styled_df, hide_index=True)


    # 2.3. Visualization Components - Comparison Bar Chart
    st.subheader("Business Unit Risk Exposure vs. Appetite & Tolerance")
    rag_colors = {'Green': '#28a745', 'Amber': '#ffc107', 'Red': '#dc3545'} # Green, Amber, Red for Plotly
    fig_bar = px.bar(
        final_df,
        x='Business Unit',
        y=['Individual_Risk_Exposure', 'Allocated Appetite', 'Absolute Risk Tolerance'],
        barmode='group',
        title="Business Unit Risk Exposure vs. Appetite & Tolerance",
        labels={
            'Business Unit': 'Business Unit',
            'value': 'Amount ($)'
        },
        height=500
    )
    # Color bars for Individual_Risk_Exposure based on Risk Status
    for i, bu in enumerate(final_df['Business Unit']):
        status = final_df.loc[final_df['Business Unit'] == bu, 'Risk Status'].iloc[0]
        fig_bar.update_traces(
            marker_color=rag_colors[status],
            selector=dict(name='Individual_Risk_Exposure', x=[bu])
        )

    # Update legend names for clarity
    new_names = {'Individual_Risk_Exposure': 'Individual Risk Exposure',
                 'Allocated Appetite': 'Allocated Appetite',
                 'Absolute Risk Tolerance': 'Absolute Risk Tolerance'}
    fig_bar.for_each_trace(lambda t: t.update(name = new_names[t.name],
                                            legendgroup = new_names[t.name],
                                            hovertemplate = t.hovertemplate.replace(t.name, new_names[t.name])))


    st.plotly_chart(fig_bar, use_container_width=True)

    # 2.3. Visualization Components - Hierarchical Visualization (Treemap)
    st.subheader("Hierarchical Risk Appetite Allocation and Exposure")

    # Prepare data for Treemap
    # Add a 'Firm' level to represent the Board Appetite
    treemap_df = pd.DataFrame({
        'Path': ['Firm'] + ['Firm/' + bu for bu in final_df['Business Unit']],
        'Value': [board_appetite] + final_df['Allocated Appetite'].tolist(),
        'Exposure': [total_firm_risk] + final_df['Individual_Risk_Exposure'].tolist(),
        'Status': ['Overall'] + final_df['Risk Status'].tolist()
    })

    # For treemap, we want to show allocated appetite by default, but potentially also exposure.
    # Plotly treemap 'color' argument changes the color of the rectangles.
    # Let's map status colors to the treemap
    treemap_color_map = {
        'Green': '#28a745', # Green
        'Amber': '#ffc107', # Amber
        'Red': '#dc3545',  # Red
        'Overall': '#6c757d' # Grey for overall firm
    }

    fig_treemap = px.treemap(
        treemap_df,
        path=['Path'],
        values='Value',  # Allocated Appetite
        color='Status',
        color_discrete_map=treemap_color_map,
        title="Hierarchical Risk Appetite Allocation (by Allocated Appetite)",
        height=600
    )
    fig_treemap.update_traces(root_color="lightgrey") # Make root distinct
    fig_treemap.data[0].textinfo = "label+value" # Show label and value on treemap
    st.plotly_chart(fig_treemap, use_container_width=True)


    # 2.3. Overall Firm Risk Profile Summary
    st.subheader("Overall Firm Risk Profile Summary")
    st.metric(label="Board Appetite", value=f"${board_appetite:,.2f}")
    st.metric(label="Total Firm Risk Profile (Aggregated Exposure)", value=f"${total_firm_risk:,.2f}")

    if total_firm_risk <= board_appetite:
        st.success(f"The Total Firm Risk Profile (${total_firm_risk:,.2f}) is within the Board Appetite (${board_appetite:,.2f}).")
    else:
        st.error(f"The Total Firm Risk Profile (${total_firm_risk:,.2f}) exceeds the Board Appetite (${board_appetite:,.2f}) by ${total_firm_risk - board_appetite:,.2f}.")
```

**`application_pages/page2.py`**
```python
import streamlit as st

def run_page2():
    st.header("Page 2: Additional Analysis")
    st.markdown("""
    This page is a placeholder for future enhancements.
    It could potentially include:
    - **Historical Risk Trends:** Analyze how risk exposures and appetites have evolved over time.
    - **Scenario Analysis:** Allow users to define different economic or operational scenarios and observe their impact on risk.
    - **Monte Carlo Simulations:** Run simulations to estimate potential future losses and their distribution.

    Stay tuned for more features!
    """)
```

**`application_pages/page3.py`**
```python
import streamlit as st

def run_page3():
    st.header("Page 3: Resources & Glossary")
    st.markdown("""
    This page is designed to provide helpful resources and definitions related to risk management.
    ### Glossary of Terms:
    - **Risk Appetite:** The amount and type of risk that an organization is willing to take in order to meet its strategic objectives.
    - **Risk Tolerance:** The acceptable level of variation around the risk appetite.
    - **Key Risk Indicators (KRIs):** Metrics used to provide an early signal of increasing risk exposures.
    - **Risk Mitigation:** Actions taken to reduce the likelihood or impact of a risk.

    ### Further Reading:
    - [COSO Enterprise Risk Management—Integrating with Strategy and Performance](https://www.coso.org/documents/erm-integratingwithstrategyandperformance-executive-summary.pdf)
    - [Basel Committee on Banking Supervision](https://www.bis.org/bcbs/index.htm)

    """)
```

### 2.5. Run the Application

Once all files are created, run the Streamlit application from your terminal (make sure your virtual environment is activated):

```bash
streamlit run app.py
```

This will open the application in your web browser, usually at `http://localhost:8501`.

## 3. Understanding the Core Logic: Risk Appetite Modeler (`page1.py`)
Duration: 0:15:00

The `application_pages/page1.py` file is the heart of the QuLab application, implementing the core risk appetite and allocation modeling logic. Let's break down its key functionalities and the data flow.

### 3.1. Application Architecture and Data Flow

The `run_page1()` function orchestrates the entire modeling process. Here's a conceptual diagram illustrating the flow of data and calculations:

```mermaid
graph TD
    A[User Inputs: Board Appetite, Allocation % for BUs] --> B{Validation: Allocation % sum to 100%?}
    B -- Valid --> C[Synthetic Data Generation: Individual Risk Exposure, Risk Tolerance Factor]
    C --> D[User Overrides: Adjust Individual Risk Exposure for BUs]
    B -- Invalid --> E[Stop / Error Message]
    D --> F[Calculate Allocated Appetite per BU]
    D --> G[Aggregate Mean Exposure & Tolerance Factor per BU]
    F & G --> H[Merge Data for Final Calculations]
    H --> I[Calculate Absolute Risk Tolerance: Allocated Appetite * Risk Tolerance Factor]
    I --> J[Determine Risk Status (RAG): Green, Amber, Red based on Exposure vs. Appetite/Tolerance]
    I --> K[Aggregate Total Firm Risk Profile: Sum of all Individual Risk Exposures]
    J & K & A --> L[Visualize & Summarize Results: Table, Bar Chart, Treemap, Firm Summary]
```

### 3.2. Key Functions and Their Roles

`page1.py` contains several helper functions that encapsulate specific pieces of logic:

#### `generate_synthetic_data()`
```python
@st.cache_data
def generate_synthetic_data():
    """Generates a pandas.DataFrame with synthetic data."""
    # ... (code for generating data)
    return df
```
This function, decorated with `@st.cache_data`, generates random but realistic data for `Individual Risk Exposure` and `Risk Tolerance Factor` for different business units. `st.cache_data` ensures that this data is generated only once (or when its inputs change), optimizing performance. The `Individual Risk Exposure` is simulated using a normal distribution, while the `Risk Tolerance Factor` is clipped between 0.1 and 1.0.

#### `validate_allocations(percentages)`
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
This critical validation function checks that the sum of all `Allocation Percentages` entered by the user is exactly 100% (with a small epsilon for floating-point precision) and that no percentage is negative. If validation fails, it raises a `ValueError`, which is caught and displayed to the user.

#### `calculate_allocated_appetite(board_appetite, allocation_percentages)`
```python
def calculate_allocated_appetite(board_appetite, allocation_percentages):
    """Computes the monetary Allocated Appetite for each business unit."""
    return [board_appetite * percentage / 100 for percentage in allocation_percentages]
```
This function takes the `Board Appetite` (firm-level risk limit) and the percentage allocations for each business unit, then calculates the specific monetary `Allocated Appetite` for each unit. For example, if `Board Appetite` is $2,000,000 and a BU gets 25% allocation, its `Allocated Appetite` is $500,000.

#### `aggregate_firm_risk(individual_exposures)`
```python
def aggregate_firm_risk(individual_exposures):
    """Sums individual risk exposures to yield the total firm risk profile."""
    return sum(individual_exposures) if individual_exposures.any() else 0
```
This simple but vital function aggregates the `Individual Risk Exposure` of all business units to determine the `Total Firm Risk Profile`. This sum is then compared against the `Board Appetite`.

#### `determine_risk_status(exposure, allocated_appetite, tolerance)`
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
This function implements the core Red, Amber, Green (RAG) logic for each business unit.
*   If `Individual Risk Exposure` is less than or equal to `Allocated Appetite`, the status is `Green`.
*   If `Individual Risk Exposure` is greater than `Allocated Appetite` but less than or equal to `Absolute Risk Tolerance`, the status is `Amber`.
*   If `Individual Risk Exposure` is greater than `Absolute Risk Tolerance`, the status is `Red`.

The `Absolute Risk Tolerance` is calculated as:
$$ \text{Absolute Risk Tolerance} = \text{Allocated Appetite} \times \text{Risk Tolerance Factor} $$

### 3.3. Data Preparation and Merging

The `run_page1` function does the following to prepare the data for visualization:
1.  **Generates Synthetic Data:** Calls `generate_synthetic_data()` to get initial `Individual Risk Exposure` and `Risk Tolerance Factor` for generic business units (BU_A, BU_B, etc.).
2.  **Maps Business Units:** Replaces generic `BU_A`, `BU_B`, etc., with human-readable names like 'Retail Banking', 'Investment Banking'.
3.  **Aggregates per Business Unit:** Groups the simulated data by `Business Unit` and calculates the mean `Individual Risk Exposure` and `Risk Tolerance Factor` for each.
4.  **Handles Missing Business Units:** Ensures all predefined business units (e.g., 'Retail Banking') are present in the summary, even if the synthetic data didn't generate entries for them, assigning default values.
5.  **Allows Overrides:** Provides `st.number_input` fields for users to manually override the simulated `Individual Risk Exposure` for each business unit. This is crucial for applying real-world data or running specific scenarios.
6.  **Calculates Allocated Appetite:** Uses `calculate_allocated_appetite()` to determine the monetary appetite for each unit based on user-defined percentages.
7.  **Merges Data:** Combines the aggregated business unit data with the calculated allocated appetites into a single DataFrame (`final_df`).
8.  **Calculates Absolute Risk Tolerance:** Adds a new column to `final_df` by multiplying `Allocated Appetite` with `Risk Tolerance Factor`.
9.  **Determines Risk Status:** Applies the `determine_risk_status()` function row-wise to `final_df` to assign a RAG status to each business unit.
10. **Calculates Total Firm Risk:** Sums up all `Individual Risk Exposure` values in `final_df` using `aggregate_firm_risk()`.

This comprehensive data preparation ensures that all necessary metrics are available for display and analysis.

<aside class="positive">
<b>Best Practice:</b> The use of `@st.cache_data` for `generate_synthetic_data` is a great example of optimizing Streamlit applications. It prevents computationally intensive data generation from running on every single user interaction, significantly improving app responsiveness.
</aside>

## 4. Exploring the User Interface and Visualizations
Duration: 0:10:00

The QuLab application's user interface is designed for intuitive interaction and clear visualization of complex risk data. Let's explore the various components and how they contribute to understanding risk appetite and allocation.

### 4.1. Defining Parameters

At the top of the `Risk Appetite Modeler` page, you'll find the parameter definition section:

*   **Board Appetite ($ Millions):** A Streamlit slider allows you to set the firm's overall risk appetite. This is a crucial input as all subsequent allocations are derived from this value.
*   **Allocation Percentages (%):** For each predefined business unit (`Retail Banking`, `Investment Banking`, `Asset Management`, `IT Operations`), you can input a percentage of the `Board Appetite` to allocate. The application actively displays the `Current sum of allocations`, and importantly, it validates that these percentages sum up to exactly 100%. If they don't, an error message appears, and further calculations are halted.
*   **Individual Risk Exposure Overrides (Optional):** Below the allocation inputs, you'll see `number_input` fields for each business unit. These display the simulated `Individual Risk Exposure` but allow you to override them with specific, actual, or hypothetical values. This feature is vital for "what-if" analysis or integrating real-world data.

<aside class="positive">
<b>Tip:</b> Experiment with different `Board Appetite` values and `Allocation Percentages` to see how the `Allocated Appetite` changes for each business unit and how it impacts their `Risk Status`.
</aside>

### 4.2. Summary of Risk Allocation & Status Table

The first major visualization is a detailed table summarizing the risk posture of each business unit.

```python
    def color_status(val):
        if val == 'Green':
            return 'background-color: #d4edda; color: #155724'
        elif val == 'Amber':
            return 'background-color: #fff3cd; color: #856404'
        elif val == 'Red':
            return 'background-color: #f8d7da; color: #721c24'
        return ''

    styled_df = final_df.style.applymap(color_status, subset=['Risk Status'])
    st.dataframe(styled_df, hide_index=True)
```

This table uses Streamlit's `st.dataframe` and Pandas styling (`.style.applymap`) to color-code the `Risk Status` column.
*   It provides a clear, row-by-row view of each `Business Unit`'s:
    *   `Individual Risk Exposure`
    *   `Risk Tolerance Factor`
    *   `Allocated Appetite`
    *   `Absolute Risk Tolerance`
    *   And most importantly, its calculated `Risk Status` (Green, Amber, or Red), highlighted for immediate visibility.

### 4.3. Business Unit Risk Exposure vs. Appetite & Tolerance Bar Chart

```python
    fig_bar = px.bar(
        final_df,
        x='Business Unit',
        y=['Individual_Risk_Exposure', 'Allocated Appetite', 'Absolute Risk Tolerance'],
        barmode='group',
        # ... (other plotting parameters)
    )
    # Color bars for Individual_Risk_Exposure based on Risk Status
    for i, bu in enumerate(final_df['Business Unit']):
        status = final_df.loc[final_df['Business Unit'] == bu, 'Risk Status'].iloc[0]
        fig_bar.update_traces(
            marker_color=rag_colors[status],
            selector=dict(name='Individual_Risk_Exposure', x=[bu])
        )
    st.plotly_chart(fig_bar, use_container_width=True)
```

This Plotly bar chart offers a comparative view. For each business unit, it plots three bars side-by-side:
*   **Individual Risk Exposure:** The actual (or overridden) risk.
*   **Allocated Appetite:** The risk limit assigned to that unit.
*   **Absolute Risk Tolerance:** The maximum acceptable risk before critical action.

The `Individual Risk Exposure` bar is dynamically colored based on its `Risk Status` (Green, Amber, Red), providing an instant visual cue of performance against limits. This is achieved by iterating through the business units and updating the `marker_color` for the `Individual_Risk_Exposure` trace in Plotly.

### 4.4. Hierarchical Risk Appetite Allocation (Treemap)

```python
    fig_treemap = px.treemap(
        treemap_df,
        path=['Path'],
        values='Value',  # Allocated Appetite
        color='Status',
        color_discrete_map=treemap_color_map,
        # ... (other plotting parameters)
    )
    st.plotly_chart(fig_treemap, use_container_width=True)
```

The treemap visualization provides a powerful hierarchical perspective of the `Allocated Appetite`.
*   The top-level `Firm` node represents the total `Board Appetite`.
*   Sub-nodes represent each `Business Unit`, with their size proportional to their `Allocated Appetite`.
*   Each business unit's rectangle is colored according to its `Risk Status` (Green, Amber, Red), reflecting its `Individual Risk Exposure` relative to its limits. This allows stakeholders to quickly identify which areas of the firm are under the most risk pressure from a top-down view.
The `treemap_df` is carefully constructed to include a 'Firm' path for the root node, showing the `Board Appetite` and `Total Firm Risk Profile`.

### 4.5. Overall Firm Risk Profile Summary

Finally, the application provides a concise summary of the firm's overall risk health:

```python
    st.metric(label="Board Appetite", value=f"${board_appetite:,.2f}")
    st.metric(label="Total Firm Risk Profile (Aggregated Exposure)", value=f"${total_firm_risk:,.2f}")

    if total_firm_risk <= board_appetite:
        st.success(...)
    else:
        st.error(...)
```

This section uses Streamlit's `st.metric` to display:
*   The `Board Appetite`.
*   The `Total Firm Risk Profile` (the sum of all individual business unit exposures).
Based on the comparison between these two values, the application displays a clear `st.success` or `st.error` message, indicating whether the firm's aggregated risk profile is within its defined board appetite. This provides a critical high-level assessment.

## 5. Placeholder Pages and Future Enhancements
Duration: 0:02:00

The QuLab application, while focused on its core risk appetite modeling, is designed with extensibility in mind. The `app.py` navigation includes placeholder pages: "Page 2" and "Page 3".

### 5.1. Page 2: Additional Analysis (`application_pages/page2.py`)

```python
import streamlit as st

def run_page2():
    st.header("Page 2: Additional Analysis")
    st.markdown("""
    This page is a placeholder for future enhancements.
    It could potentially include:
    - **Historical Risk Trends:** Analyze how risk exposures and appetites have evolved over time.
    - **Scenario Analysis:** Allow users to define different economic or operational scenarios and observe their impact on risk.
    - **Monte Carlo Simulations:** Run simulations to estimate potential future losses and their distribution.

    Stay tuned for more features!
    """)
```

This page serves as a conceptual blueprint for expanding the application's analytical capabilities. As suggested in its content, future enhancements could include:
*   **Historical Trends:** Integrating time-series data to visualize how risk appetites and exposures change over periods, identifying trends and recurring patterns.
*   **Scenario Analysis:** Allowing users to define specific future scenarios (e.g., economic downturn, regulatory changes, new market entry) and model their potential impact on risk profiles.
*   **Monte Carlo Simulations:** Implementing stochastic simulations to provide a probabilistic view of potential future losses or risk events, offering a more nuanced understanding of uncertainty.

These additions would significantly enhance the model's predictive and strategic planning utility.

### 5.2. Page 3: Resources & Glossary (`application_pages/page3.py`)

```python
import streamlit as st

def run_page3():
    st.header("Page 3: Resources & Glossary")
    st.markdown("""
    This page is designed to provide helpful resources and definitions related to risk management.
    ### Glossary of Terms:
    - **Risk Appetite:** The amount and type of risk that an organization is willing to take in order to meet its strategic objectives.
    - **Risk Tolerance:** The acceptable level of variation around the risk appetite.
    - **Key Risk Indicators (KRIs):** Metrics used to provide an early signal of increasing risk exposures.
    - **Risk Mitigation:** Actions taken to reduce the likelihood or impact of a risk.

    ### Further Reading:
    - [COSO Enterprise Risk Management—Integrating with Strategy and Performance](https://www.coso.org/documents/erm-integratingwithstrategyandperformance-executive-summary.pdf)
    - [Basel Committee on Banking Supervision](https://www.bis.org/bcbs/index.htm)

    """)
```

This page is a valuable educational resource within the application. It provides:
*   **Glossary of Terms:** Clear definitions of key risk management concepts, ensuring that users (especially those new to the domain) understand the terminology used throughout the application.
*   **Further Reading:** Links to authoritative external resources (like COSO and Basel Committee), encouraging users to delve deeper into the theoretical and regulatory aspects of risk management.

This page underscores the application's role not just as a modeling tool, but also as an educational platform for risk professionals.

## 6. Conclusion and Next Steps
Duration: 0:02:00

Congratulations! You have successfully explored the QuLab application, a practical Streamlit tool for understanding and modeling risk appetite and allocation within an organizational context.

### Key Takeaways:

*   **Holistic Risk View:** The application demonstrates how a top-down `Board Appetite` is cascaded into `Allocated Appetites` for individual business units, and how their `Individual Risk Exposures` aggregate to form the `Total Firm Risk Profile`.
*   **Visual Assessment:** The RAG status system, combined with interactive charts and tables, provides an intuitive and immediate visual assessment of risk performance against defined limits.
*   **Modularity:** The application's structure, with a main `app.py` and separate pages in `application_pages/`, promotes modularity and ease of extension.
*   **Streamlit Capabilities:** You've seen how Streamlit's widgets (`st.slider`, `st.number_input`, `st.dataframe`, `st.plotly_chart`, `st.metric`) and caching (`st.cache_data`) enable rapid development of interactive data applications.

### Next Steps for Developers:

*   **Enhance Synthetic Data:** Improve `generate_synthetic_data` to allow more complex distributions or correlations between business units.
*   **Database Integration:** Replace synthetic data with actual data loaded from a database (e.g., SQLite, PostgreSQL) or a cloud service.
*   **Advanced Scenario Planning:** Implement the ideas for `Page 2`, allowing users to define and run custom risk scenarios.
*   **User Authentication:** For a production environment, add user authentication to control access to the application.
*   **Audit Trail:** Implement logging to track changes made by users to parameters and observe the resulting risk status changes.
*   **More Granular Allocations:** Extend the allocation model to support sub-units within business units or different risk types (e.g., operational, credit, market risk).
*   **Dynamic Business Units:** Allow users to add or remove business units dynamically, instead of having a fixed list.

This codelab has provided a solid foundation for understanding the QuLab application. Feel free to fork the code, experiment with its functionalities, and extend it to suit more complex risk management scenarios!
