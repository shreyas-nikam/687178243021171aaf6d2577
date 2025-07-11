
import streamlit as st
st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()
st.markdown("""
In this lab, we explore the crucial concepts of **Risk Appetite** and **Risk Allocation** within an organization.
Understanding how a firm defines its overall risk appetite and then cascades it down to individual business units is
fundamental for effective risk management and strategic decision-making.

### Learning Outcomes:
- Define and set a firm's top-level `Board Appetite`.
- Simulate the hierarchical allocation of risk appetite across various business units.
- Understand the aggregation of individual risk exposures and their comparison against allocated limits.
- Visualize risk status using a clear **Red, Amber, Green (RAG)** system.
- Evaluate the `Total Firm Risk Profile` against the `Board Appetite`.

### Application Features:
- **Interactive Inputs:** Adjust `Board Appetite` and `Allocation Percentages` in real-time.
- **Dynamic Visualizations:** See immediate updates in tables and charts (Bar Chart, Treemap) as inputs change.
- **Risk Status Monitoring:** Instant feedback on whether business units are within, nearing, or exceeding their risk limits.
- **Comprehensive Summary:** A clear overview of the firm's total risk profile against its strategic appetite.

### Underlying Concepts:
- **Board Appetite:** The maximum level of risk a firm is willing to accept to achieve its strategic objectives.
- **Risk Allocation:** The process of distributing the overall Board Appetite to different segments, departments, or business units.
- **Individual Risk Exposure:** The actual or estimated losses incurred by a specific business unit due to various risks.
- **Risk Tolerance:** The acceptable deviation from the allocated appetite, often expressed as a factor or absolute amount.
- **RAG Status:** A traffic-light system (Red, Amber, Green) used for quick visual assessment of risk performance.

This application provides a practical, hands-on tool to interact with these concepts and observe their interplay.
""")
# Your code starts here
page = st.sidebar.selectbox(label="Navigation", options=["Risk Appetite & Allocation Modeler (Page 1)", "Page 2", "Page 3"])

if page == "Risk Appetite & Allocation Modeler (Page 1)":
    from application_pages.page1 import run_page
    run_page()
elif page == "Page 2":
    # Placeholder for Page 2
    st.markdown("""
    ## Page 2 - Coming Soon!
    This page is a placeholder for future features related to risk modeling.
    """)
elif page == "Page 3":
    # Placeholder for Page 3
    st.markdown("""
    ## Page 3 - Coming Soon!
    This page is a placeholder for future features related to risk analysis.
    """)
# Your code ends
