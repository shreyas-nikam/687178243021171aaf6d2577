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
    
    # Helpful tip for beginners
    st.info("**Pro Tip**: Start by adjusting the Board Appetite slider and watch how all calculations update in real-time!")
    
    # Business Units Definition
    business_units_list = ['Retail Banking', 'Investment Banking', 'Asset Management', 'IT Operations']
    st.subheader("1. Define Board Appetite and Allocation")
    st.markdown(
        "Set the *maximum acceptable annual loss* for the entire firm, then apportion that limit to each business unit. "
        "The sum of allocations must equal **100%**. Think of this as dividing your risk budget among different departments."
    )


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
    st.markdown(
        "View or override the simulated individual risk exposure for each unit (e.g., actual annual losses). "
        "**Try this**: Change one value to see how it affects the risk status and visualizations below!"
    )
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
    st.markdown(
        "Green means exposure is **within** allocated appetite.  \n"
        "Amber means it **exceeds appetite** but is **within tolerance**.  \n"
        "Red means it **breaches tolerance** – management action required."
    )
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

    styled_df = final_df.style.map(color_status, subset=['Risk Status'])
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
    import numpy as np
    for i, bu in enumerate(final_df['Business Unit']):
        status = final_df.loc[final_df['Business Unit'] == bu, 'Risk Status'].iloc[0]
        fig_bar.update_traces(
            marker_color=[rag_colors[status]],
            selector=lambda t: t.name == 'Individual_Risk_Exposure'
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
    st.metric(label="Board's Appetite", value=f"${board_appetite:,.2f}")
    st.metric(label="Total Firm Risk Profile (Aggregated Exposure)", value=f"${total_firm_risk:,.2f}")

    if total_firm_risk <= board_appetite:
        st.success(f"The Total Firm Risk Profile (${total_firm_risk:,.2f}) is within the Board's Appetite (${board_appetite:,.2f}).")
    else:
        st.error(f"The Total Firm Risk Profile (${total_firm_risk:,.2f}) exceeds the Board's Appetite (${board_appetite:,.2f}) by ${total_firm_risk - board_appetite:,.2f}.")

    st.markdown("""### Further Reading:

- [Basel Committee on Banking Supervision](https://www.bis.org/bcbs/index.htm)
    """)