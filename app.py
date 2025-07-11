
import streamlit as st
st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()
st.markdown(r"""
In this lab, we delve into the foundational concepts of **Risk Appetite and Allocation**. Understanding how an organization defines, cascades, and monitors its risk appetite is crucial for effective risk management. This application provides an interactive environment to:

*   **Define Board Appetite:** Set the overarching risk tolerance for the entire firm.
*   **Allocate Appetite:** Distribute the firm's total risk appetite across various business units.
*   **Monitor Individual Exposures:** Compare actual risk exposures against allocated limits.
*   **Visualize Risk Status:** Use a Red, Amber, Green (RAG) system to highlight units within or exceeding their risk boundaries.
*   **Aggregate Firm-wide Risk:** See how individual unit exposures contribute to the total firm risk profile.

Through this interactive tool, you can explore "what-if" scenarios by adjusting key parameters and observing their immediate impact on risk allocation and status. The goal is to provide a clear and intuitive understanding of how risk appetite frameworks operate in practice, bridging strategic objectives with operational realities.

We will be covering these topics through three interactive pages:
*   **Page 1: Risk Appetite & Allocation Modeler:** The core simulation environment for defining, allocating, and monitoring risk appetite.
*   **Page 2: Types of Risk:** An overview of different categories of risk faced by financial institutions.
*   **Page 3: Basic VaR Calculation:** An introduction to Value at Risk (VaR) as a key risk measure.
""")

page = st.sidebar.selectbox(label="Navigation", options=["Risk Appetite & Allocation Modeler", "Types of Risk", "Basic VaR Calculation"])

if page == "Risk Appetite & Allocation Modeler":
    from application_pages.page1 import run_page1
    run_page1()
elif page == "Types of Risk":
    from application_pages.page2 import run_page2
    run_page2()
elif page == "Basic VaR Calculation":
    from application_pages.page3 import run_page3
    run_page3()
