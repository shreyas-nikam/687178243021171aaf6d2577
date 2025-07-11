
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
    return sum(individual_exposures) if individual_exposures else 0

# 4.6. Determination of Risk Status (RAG Logic)
def determine_risk_status(exposure, allocated_appetite, tolerance):
    """Applies RAG logic to determine risk status."""
    if exposure <= allocated_appetite:
        return 'Green'
    elif exposure <= tolerance: # This implies allocated_appetite < exposure <= tolerance
        return 'Amber'
    else: # This implies tolerance < exposure
        return 'Red'

def run_page():
    st.header("Risk Appetite & Allocation Modeler")
    st.markdown("""
    This interactive tool allows you to simulate and visualize how a firm's overall risk appetite
    is cascaded down to individual business units and how their actual risk exposures compare
    against these allocated limits.
    """)

    st.markdown("""
    ### 1. Define Board Appetite
    The `Board Appetite` represents the maximum acceptable annual operational loss for the entire firm.
    """)
    # 2.2. Input Widgets and Controls - Board Appetite
    board_appetite = st.slider(
        "Set Board Appetite (in millions of $)",
        min_value=10.0,
        max_value=100.0,
        value=50.0,
        step=5.0,
        help="Set the maximum acceptable annual operational loss for the entire firm."
    )
    board_appetite_actual = board_appetite * 1_000_000 # Convert to actual value for calculations

    st.markdown("""
    ### 2. Cascading Allocation Percentages
    Allocate a percentage of the `Board Appetite` to each business unit.
    The sum of all allocation percentages **must equal 100%**.
    """)

    business_units_list = ['Retail Banking', 'Investment Banking', 'Asset Management', 'IT Operations']
    initial_allocations = {'Retail Banking': 30, 'Investment Banking': 40, 'Asset Management': 15, 'IT Operations': 15}

    allocation_percentages = {}
    cols = st.columns(len(business_units_list))
    for i, bu in enumerate(business_units_list):
        with cols[i]:
            allocation_percentages[bu] = st.number_input(
                f"Allocation for {bu} (%)",
                min_value=0,
                max_value=100,
                value=initial_allocations.get(bu, 0),
                step=1,
                key=f"alloc_{bu}",
                help="Allocate a percentage of the Board Appetite to this business unit."
            )

    current_total_allocation = sum(allocation_percentages.values())
    st.info(f"Current Total Allocation: {current_total_allocation}%")

    try:
        validate_allocations(list(allocation_percentages.values()))
        st.success("Allocation percentages sum to 100%! Ready for calculations.")
        allocation_valid = True
    except ValueError as e:
        st.error(f"Validation Error: {e}")
        st.warning("Please adjust allocation percentages to sum to 100%.")
        allocation_valid = False

    st.markdown("""
    ### 3. Individual Risk Exposure & Tolerance
    View or override the simulated individual risk exposure and tolerance factor for each unit.
    """)

    # Data Preparation
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
    for bu in business_units_list:
        if bu not in bu_summary['Business Unit'].values:
            bu_summary = pd.concat([bu_summary, pd.DataFrame([{'Business Unit': bu, 'Individual_Risk_Exposure': 0, 'Risk_Tolerance_Factor': 0}])], ignore_index=True)
    bu_summary = bu_summary.set_index('Business Unit').loc[business_units_list].reset_index() # Reorder

    # Optional User Override for Individual Risk Exposure
    user_overrides = {}
    for i, bu in enumerate(business_units_list):
        col1, col2 = st.columns(2)
        with col1:
            default_exposure = bu_summary[bu_summary['Business Unit'] == bu]['Individual_Risk_Exposure'].iloc[0]
            user_overrides[bu] = st.number_input(
                f"Override Exposure for {bu} ($)",
                min_value=0,
                value=int(default_exposure),
                step=1000,
                key=f"override_exp_{bu}",
                help=f"View or override the simulated individual risk exposure for {bu} (e.g., actual annual losses)."
            )
        with col2:
            st.markdown(f"Simulated Risk Tolerance Factor for {bu}: **{bu_summary[bu_summary['Business Unit'] == bu]['Risk_Tolerance_Factor'].iloc[0]:.2f}**")

    # Update bu_summary with user overrides
    bu_summary['Individual_Risk_Exposure'] = bu_summary['Business Unit'].map(user_overrides)


    if allocation_valid:
        st.markdown("""
        ### 4. Risk Allocation & Status Summary
        Here's a detailed breakdown of allocated appetite, absolute risk tolerance, and the
        current risk status (Red, Amber, Green) for each business unit.
        """)

        # Calculate Allocated Appetite
        allocated_appetites = calculate_allocated_appetite(board_appetite_actual, list(allocation_percentages.values()))
        allocated_df = pd.DataFrame({
            'Business Unit': business_units_list,
            'Allocated Appetite': allocated_appetites
        })

        # Merge Data
        final_df = pd.merge(bu_summary, allocated_df, on='Business Unit')

        # Calculate Absolute Risk Tolerance
        final_df['Absolute Risk Tolerance'] = final_df['Allocated Appetite'] * final_df['Risk_Tolerance_Factor']

        # Determine Risk Status
        final_df['Risk Status'] = final_df.apply(
            lambda row: determine_risk_status(
                row['Individual_Risk_Exposure'],
                row['Allocated Appetite'],
                row['Absolute Risk Tolerance']
            ), axis=1
        )

        # Summary Table
        st.dataframe(final_df.style.applymap(
            lambda x: 'background-color: #d4edda' if x == 'Green' else ('background-color: #fff3cd' if x == 'Amber' else 'background-color: #f8d7da'),
            subset=['Risk Status']
        ).format({
            'Individual_Risk_Exposure': '${:,.0f}',
            'Allocated Appetite': '${:,.0f}',
            'Absolute Risk Tolerance': '${:,.0f}'
        }))

        st.markdown("""
        **Risk Status Logic:**
        - **Green:** $\text{Exposure} \le \text{Allocated Appetite}$
        - **Amber:** $\text{Allocated Appetite} < \text{Exposure} \le \text{Absolute Risk Tolerance}$
        - **Red:** $\text{Exposure} > \text{Absolute Risk Tolerance}$
        """)

        st.markdown("""
        ### 5. Visualizations
        """)

        # Comparison Bar Chart
        st.subheader("Business Unit Risk Exposure vs. Appetite & Tolerance")
        # Define color map for RAG status
        rag_color_map = {'Green': 'green', 'Amber': 'orange', 'Red': 'red'}

        fig_bar = px.bar(
            final_df,
            x='Business Unit',
            y=['Individual_Risk_Exposure', 'Allocated Appetite', 'Absolute Risk Tolerance'],
            barmode='group',
            title='Business Unit Risk Exposure vs. Appetite & Tolerance',
            labels={
                'value': 'Amount ($)',
                'variable': 'Metric'
            },
            color='Risk Status',
            color_discrete_map=rag_color_map,
            hover_data={
                'Individual_Risk_Exposure': ':, .0f',
                'Allocated Appetite': ':, .0f',
                'Absolute Risk Tolerance': ':, .0f',
                'Risk Status': True
            }
        )
        # Update layout for better readability and potentially larger font
        fig_bar.update_layout(
            legend_title_text='Metric',
            font=dict(size=12),
            height=500
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Hierarchical Visualization (Treemap)
        st.subheader("Hierarchical Risk Appetite Allocation and Exposure")
        # For treemap, we need a hierarchical structure
        # Create a dataframe suitable for treemap
        treemap_data = pd.DataFrame({
            'id': ['Firm'] + business_units_list,
            'parent': ['', 'Firm', 'Firm', 'Firm', 'Firm'],
            'value': [board_appetite_actual] + allocated_appetites,
            'name': ['Board Appetite'] + [f"{bu} ({allocation_percentages[bu]}%)" for bu in business_units_list],
            'type': ['Board Appetite'] + ['Allocated Appetite'] * len(business_units_list)
        })

        # Add individual risk exposure for a more detailed view if needed, but for simplicity,
        # let's stick to showing allocation and exposure as a color on the allocated part
        # A more complex treemap could show exposure as a sub-segment.
        # For this, let's use a simpler approach of mapping status colors to allocated appetite.
        final_df['Exposure_vs_Appetite'] = final_df['Individual_Risk_Exposure'] / final_df['Allocated Appetite']

        # Add aggregated exposure to treemap data (optional, for color or size if represented)
        # Let's add exposure as a separate series or use it for color if the treemap supports it directly
        # For plotly treemap, value determines size, color determines color.
        # Let's create a combined df for the treemap to represent allocated appetite and color by status
        treemap_combined_df = final_df[['Business Unit', 'Allocated Appetite', 'Risk Status', 'Individual_Risk_Exposure']].copy()
        treemap_combined_df.rename(columns={'Business Unit': 'Labels', 'Allocated Appetite': 'Values'}, inplace=True)
        treemap_combined_df['Parents'] = 'Firm'
        treemap_combined_df.loc[len(treemap_combined_df)] = ['Firm', board_appetite_actual - treemap_combined_df['Values'].sum(), 'Green', 0, ''] # Remaining from total
        treemap_combined_df.loc[len(treemap_combined_df)] = ['Total Board Appetite', board_appetite_actual, 'Green', 0, ''] # Root

        fig_treemap = px.treemap(
            final_df,
            path=[px.Constant("Board Appetite"), 'Business Unit'],
            values='Allocated Appetite',
            color='Risk Status',
            color_discrete_map={
                'Green': 'green',
                'Amber': 'orange',
                'Red': 'red',
                '(?)': 'lightgrey' # For cases where status might be unknown
            },
            title="Hierarchical Risk Appetite Allocation and Exposure",
            custom_data=['Individual_Risk_Exposure', 'Absolute Risk Tolerance'] # For hover info
        )
        fig_treemap.update_traces(
            root_color="lightgrey",
            marker_line_width=1,
            marker_line_color='black',
            textinfo="label+value+percent entry"
        )
        fig_treemap.update_layout(margin=dict(t=50, l=0, r=0, b=0), font=dict(size=12))
        fig_treemap.data[0].texttemplate = "%{label}<br>%{value:$,.0f}<br>%{percentParent:.1%}"
        fig_treemap.data[0].hovertemplate = (
            "<b>Business Unit:</b> %{label}<br>"
            "<b>Allocated Appetite:</b> %{value:$,.0f}<br>"
            "<b>Individual Exposure:</b> %{customdata[0]:$,.0f}<br>"
            "<b>Absolute Tolerance:</b> %{customdata[1]:$,.0f}<br>"
            "<b>Risk Status:</b> %{color}<extra></extra>"
        )

        st.plotly_chart(fig_treemap, use_container_width=True)

        st.markdown("""
        ### 6. Overall Firm Risk Profile Summary
        """)
        # Overall Firm Risk Profile Summary
        total_firm_risk_profile = aggregate_firm_risk(final_df['Individual_Risk_Exposure'].tolist())

        st.metric(label="Board Appetite", value=f"${board_appetite_actual:,.0f}")
        st.metric(label="Total Firm Risk Profile", value=f"${total_firm_risk_profile:,.0f}")

        if total_firm_risk_profile <= board_appetite_actual:
            st.success(f"**Conclusion:** The Total Firm Risk Profile (${total_firm_risk_profile:,.0f}) is **within** the Board Appetite (${board_appetite_actual:,.0f}).")
        else:
            st.error(f"**Conclusion:** The Total Firm Risk Profile (${total_firm_risk_profile:,.0f}) **exceeds** the Board Appetite (${board_appetite_actual:,.0f}). Immediate action may be required.")
    else:
        st.warning("Please resolve allocation percentage validation errors to see the full analysis.")
