
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def generate_synthetic_data():
    \"\"\"Generates a pandas.DataFrame with synthetic data.\"\"\"
    num_rows = 100
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

def validate_allocations(percentages):
    \"\"\"Ensures allocation percentages sum to 100% and are non-negative.\"\"\"
    epsilon = 1e-6
    total = sum(percentages)
    if not all(p >= 0 for p in percentages):
        raise ValueError("Allocation percentages must be non-negative.")
    if not (100 - epsilon <= total <= 100 + epsilon):
        raise ValueError("Allocation percentages must sum to 100%.")
    return None

def calculate_allocated_appetite(board_appetite, allocation_percentages):
    \"\"\"Computes the monetary Allocated Appetite for each business unit.\"\"\"
    return [board_appetite * percentage / 100 for percentage in allocation_percentages]

def aggregate_firm_risk(individual_exposures):
    \"\"\"Sums individual risk exposures to yield the total firm risk profile.\"\"\"
    return sum(individual_exposures) if individual_exposures.any() else 0

def determine_risk_status(exposure, allocated_appetite, tolerance):
    \"\"\"Applies RAG logic to determine risk status.\"\"\"
    if exposure <= allocated_appetite:
        return 'Green'
    elif exposure <= tolerance: # This implies allocated_appetite < exposure <= tolerance
        return 'Amber'
    else: # This implies tolerance < exposure
        return 'Red'

def run_page1():
    st.title("Risk Appetite & Allocation Modeler")

    st.markdown(r\"\"\"
    Welcome to the **Risk Appetite & Allocation Modeler**! This interactive tool allows you to simulate how a firm's overall risk appetite is defined, cascaded down to individual business units, and then monitored against actual risk exposures.

    ### Learning Outcomes:
    *   Understand the concept of **Board Appetite** and its significance.
    *   Learn how **Risk Appetite** is allocated across different business units.
    *   Visualize the comparison between **Individual Risk Exposures** and **Allocated Appetite/Tolerance**.
    *   Interpret **Risk Status** using a Red, Amber, Green (RAG) system.
    *   See how individual unit risks aggregate to form the **Total Firm Risk Profile**.

    ### Core Concepts:
    *   **Board Appetite:** The maximum level of risk a firm is willing to accept to achieve its strategic objectives.
    *   **Allocated Appetite:** The portion of the Board Appetite assigned to a specific business unit or function.
    *   **Individual Risk Exposure:** The actual risk incurred by a business unit (e.g., operational losses, credit defaults).
    *   **Risk Tolerance Factor:** A multiplier applied to Allocated Appetite to determine the Absolute Risk Tolerance, allowing for some buffer beyond the strict appetite limit before reaching a critical state.
    *   **Absolute Risk Tolerance:** The maximum acceptable exposure for a business unit, derived from its Allocated Appetite and Risk Tolerance Factor.

    The primary formula for **Allocated Appetite** is:
    $$\text{Allocated Appetite}_i = \text{Board Appetite} \times \frac{\text{Allocation Percentage}_i}{100}$$

    The **Absolute Risk Tolerance** for each unit is calculated as:
    $$\text{Absolute Risk Tolerance}_i = \text{Allocated Appetite}_i \times \text{Risk Tolerance Factor}_i$$

    The **Total Firm Risk Profile** is the sum of all individual risk exposures:
    $$\text{Total Firm Risk Profile} = \sum_{i=1}^{n} \text{Individual Risk Exposure}_i$$

    The **Risk Status** is determined using the following RAG (Red, Amber, Green) logic:
    *   If $\text{exposure} \le \text{allocated\_appetite}$, status is 'Green'.
    *   If $\text{allocated\_appetite} < \text{exposure} \le \text{tolerance}$, status is 'Amber'.
    *   If $\text{exposure} > \text{tolerance}$, status is 'Red'.
    \"\"\"
    )

    st.divider()

    st.header("1. Define Board Appetite")
    board_appetite = st.slider(
        "Set Board Appetite (in millions $)",
        min_value=10.0,
        max_value=500.0,
        value=100.0,
        step=5.0,
        help="Set the maximum acceptable annual operational loss for the entire firm."
    ) * 1_000_000 # Convert to actual millions

    st.header("2. Cascading Allocation Percentages")
    st.markdown("Allocate a percentage of the Board Appetite to each business unit. **The sum must equal 100%.**")

    # Business units mapping
    bu_mapping = {
        'BU_A': 'Retail Banking',
        'BU_B': 'Investment Banking',
        'BU_C': 'Asset Management',
        'BU_D': 'IT Operations'
    }
    business_units_list = list(bu_mapping.values())

    allocation_percentages = {}
    cols = st.columns(len(business_units_list))
    for i, bu in enumerate(business_units_list):
        with cols[i]:
            allocation_percentages[bu] = st.number_input(
                f"{bu} (%)",
                min_value=0.0,
                max_value=100.0,
                value=25.0, # Initial equal allocation
                step=1.0,
                key=f"alloc_{bu}",
                help=f"Percentage of Board Appetite allocated to {bu}."
            )

    current_allocations = list(allocation_percentages.values())
    try:
        validate_allocations(current_allocations)
        st.success("Allocation percentages sum to 100%.")
    except ValueError as e:
        st.error(f"Allocation Error: {e}")
        st.stop() # Stop execution if allocations are invalid

    st.header("3. Individual Risk Exposure & Tolerance")
    st.markdown("View or override the simulated individual risk exposure and tolerance factor for each unit. (e.g., actual annual losses).")

    # Generate synthetic data and aggregate
    simulated_data = generate_synthetic_data()
    simulated_data['Business Unit'] = simulated_data['Business Unit'].map(bu_mapping)

    bu_summary = simulated_data.groupby('Business Unit').agg(
        Individual_Risk_Exposure=('Individual Risk Exposure', 'mean'),
        Risk_Tolerance_Factor=('Risk Tolerance Factor', 'mean')
    ).reset_index()

    # Ensure all expected business units are present, even if no synthetic data for them
    # (This ensures input widgets are created for all units)
    for bu in business_units_list:
        if bu not in bu_summary['Business Unit'].values:
            bu_summary = pd.concat([bu_summary, pd.DataFrame([{'Business Unit': bu, 'Individual_Risk_Exposure': 0, 'Risk_Tolerance_Factor': 0.7}])], ignore_index=True)
    bu_summary = bu_summary.set_index('Business Unit').reindex(business_units_list).reset_index() # Maintain order

    # User override for Individual Risk Exposure
    user_exposures = {}
    user_tolerance_factors = {}
    for bu in business_units_list:
        default_exposure = bu_summary[bu_summary['Business Unit'] == bu]['Individual_Risk_Exposure'].iloc[0]
        default_tolerance_factor = bu_summary[bu_summary['Business Unit'] == bu]['Risk_Tolerance_Factor'].iloc[0]

        col1, col2 = st.columns(2)
        with col1:
            user_exposures[bu] = st.number_input(
                f"Override {bu} Exposure ($)",
                min_value=0.0,
                value=float(default_exposure),
                step=1000.0,
                key=f"exposure_{bu}",
                help=f"Override the simulated individual risk exposure for {bu}."
            )
        with col2:
            user_tolerance_factors[bu] = st.number_input(
                f"Override {bu} Tolerance Factor",
                min_value=0.1,
                max_value=1.0,
                value=float(default_tolerance_factor),
                step=0.05,
                key=f"tolerance_{bu}",
                help=f"Override the simulated risk tolerance factor for {bu} (0.1 to 1.0)."
            )

    # Prepare data for final calculations
    final_df_data = []
    for bu in business_units_list:
        allocated_appetite_val = calculate_allocated_appetite(board_appetite, [allocation_percentages[bu]])[0]
        individual_exposure_val = user_exposures[bu]
        risk_tolerance_factor_val = user_tolerance_factors[bu]
        absolute_risk_tolerance_val = allocated_appetite_val * risk_tolerance_factor_val

        final_df_data.append({
            "Business Unit": bu,
            "Individual_Risk_Exposure": individual_exposure_val,
            "Allocated Appetite": allocated_appetite_val,
            "Absolute Risk Tolerance": absolute_risk_tolerance_val,
            "Risk Tolerance Factor": risk_tolerance_factor_val
        })

    final_df = pd.DataFrame(final_df_data)

    # Determine Risk Status
    final_df['Risk Status'] = final_df.apply(
        lambda row: determine_risk_status(
            row['Individual_Risk_Exposure'],
            row['Allocated Appetite'],
            row['Absolute Risk Tolerance']
        ),
        axis=1
    )

    # Define color mapping for RAG status
    color_map = {'Green': 'green', 'Amber': 'orange', 'Red': 'red'}

    st.header("4. Summary & Visualizations")

    st.subheader("Business Unit Risk Summary")
    st.dataframe(final_df.style.apply(lambda x: [f'background-color: {color_map[v]}' for v in x]
                                      if x.name == 'Risk Status' else [''] * len(x), axis=1))

    st.subheader("Business Unit Risk Exposure vs. Appetite & Tolerance")
    fig_bar = px.bar(
        final_df,
        x='Business Unit',
        y=['Individual_Risk_Exposure', 'Allocated Appetite', 'Absolute Risk Tolerance'],
        barmode='group',
        title="Business Unit Risk Exposure vs. Appetite & Tolerance",
        labels={'value': 'Amount ($)', 'variable': 'Metric'},
        color='Risk Status',
        color_discrete_map=color_map # Apply RAG colors to exposure bars
    )
    # Customize individual risk exposure bars to reflect RAG status more explicitly
    # This part requires more advanced plotly, for simplicity, we map color based on the 'color' argument above.
    # If explicit color mapping per bar based on 'Risk Status' is needed, it would involve modifying traces.
    # px.bar will handle this correctly for the `Individual_Risk_Exposure` group if `color` is based on `Risk Status`.
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Hierarchical Risk Appetite Allocation and Exposure")
    # Prepare data for treemap: Add a 'Firm' level for the root
    treemap_df = final_df.copy()
    treemap_df['Parent'] = 'Firm'
    treemap_df['Amount'] = treemap_df['Allocated Appetite']

    # For hierarchical visualization, it's often better to show the allocated appetite first, then potentially exposures.
    # Let's create a DataFrame suitable for a treemap showing Board Appetite -> Allocated Appetite
    # To also show exposure, we might need a multi-level treemap or a different visualization.
    # For simplicity, let's show allocated appetite and highlight exposure status.

    # Option 1: Treemap showing Allocation
    treemap_data = [
        {'id': 'Firm', 'parent': '', 'name': 'Board Appetite', 'value': board_appetite, 'type': 'Appetite'},
    ]
    for idx, row in final_df.iterrows():
        treemap_data.append({
            'id': row['Business Unit'],
            'parent': 'Firm',
            'name': f"{row['Business Unit']} (Allocated: ${row['Allocated Appetite']:.0f}, Exp: ${row['Individual_Risk_Exposure']:.0f}, Status: {row['Risk Status']})",
            'value': row['Allocated Appetite'], # Size by allocated appetite
            'type': 'Allocated Appetite',
            'status': row['Risk Status'] # Add status for coloring
        })
    treemap_flat_df = pd.DataFrame(treemap_data)

    fig_treemap = px.treemap(
        treemap_flat_df,
        names='name',
        parents='parent',
        values='value',
        color='status', # Color by risk status of the business unit
        color_discrete_map={'(?)': 'lightgrey', 'Green': 'green', 'Amber': 'orange', 'Red': 'red'},
        title="Hierarchical Risk Appetite Allocation and Exposure",
        hover_data=['value'],
    )
    st.plotly_chart(fig_treemap, use_container_width=True)


    st.subheader("Overall Firm Risk Profile Summary")
    total_firm_risk_profile = aggregate_firm_risk(final_df['Individual_Risk_Exposure'])

    st.metric(label="Board Appetite", value=f"${board_appetite:,.2f}")
    st.metric(label="Total Firm Risk Profile (Aggregated Exposure)", value=f"${total_firm_risk_profile:,.2f}")

    if total_firm_risk_profile <= board_appetite:
        st.success(f"Conclusion: The Total Firm Risk Profile (${total_firm_risk_profile:,.2f}) is **within** the Board Appetite (${board_appetite:,.2f}). This indicates the firm's overall risk exposure is currently acceptable.")
    else:
        st.error(f"Conclusion: The Total Firm Risk Profile (${total_firm_risk_profile:,.2f}) **exceeds** the Board Appetite (${board_appetite:,.2f}). This suggests the firm's overall risk exposure is currently too high and requires attention.")

