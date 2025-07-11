
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
