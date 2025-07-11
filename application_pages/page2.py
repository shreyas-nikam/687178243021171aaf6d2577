
import streamlit as st

def run_page2():
    st.title("Types of Risk")
    st.markdown(r\"\"\"
    In the world of finance and business, risk is inherent in every operation and decision. Understanding the various types of risk is fundamental to effective risk management. This page provides an overview of common risk categories encountered by organizations, particularly financial institutions.

    ### Key Categories of Risk:

    1.  **Credit Risk:**
        *   **Definition:** The risk of loss due to a borrower's or counterparty's failure to meet its financial obligations.
        *   **Examples:**
            *   A bank's loan customer defaults on their mortgage.
            *   A company's bond issuer fails to make interest or principal payments.
            *   A counterparty in a derivatives trade defaults before settlement.
        *   **Mitigation:** Diversification, collateral, credit ratings, credit default swaps.

    2.  **Market Risk:**
        *   **Definition:** The risk of losses in positions arising from movements in market prices. This includes changes in interest rates, exchange rates, equity prices, and commodity prices.
        *   **Examples:**
            *   A stock portfolio loses value due to a general market downturn.
            *   A bond portfolio's value declines as interest rates rise.
            *   Currency fluctuations negatively impact the value of foreign investments.
        *   **Measurement:** Value at Risk (VaR), Stress Testing.

    3.  **Operational Risk:**
        *   **Definition:** The risk of loss resulting from inadequate or failed internal processes, people and systems, or from external events.
        *   **Examples:**
            *   System failure leading to trading errors.
            *   Fraud by an employee.
            *   A natural disaster disrupting business operations.
            *   Cybersecurity breaches.
        *   **Mitigation:** Robust internal controls, disaster recovery planning, employee training, cybersecurity measures.

    4.  **Liquidity Risk:**
        *   **Definition:** The risk that an entity will not be able to meet its short-term financial obligations without incurring unacceptable losses. It can manifest as funding liquidity risk (inability to raise funds) or market liquidity risk (inability to sell assets quickly without price concession).
        *   **Examples:**
            *   A bank cannot meet customer withdrawal demands.
            *   A firm cannot sell illiquid assets quickly enough to cover maturing liabilities.
        *   **Mitigation:** Maintaining sufficient cash reserves, diversified funding sources, contingency funding plans.

    5.  **Strategic Risk:**
        *   **Definition:** The risk arising from adverse business decisions, improper implementation of decisions, or lack of responsiveness to changes in the business environment.
        *   **Examples:**
            *   Launching a product that fails to gain market acceptance.
            *   Failure to adapt to new technologies or changing consumer preferences.
            *   Poor mergers and acquisitions decisions.
        *   **Mitigation:** Strategic planning, market analysis, robust governance frameworks.

    6.  **Reputational Risk:**
        *   **Definition:** The risk of damage to a company's reputation, which can lead to a decline in customer trust, loss of business, or regulatory scrutiny.
        *   **Examples:**
            *   A major data breach leading to negative public perception.
            *   Legal or ethical misconduct by senior management.
            *   Negative media coverage due to product failures.
        *   **Mitigation:** Ethical conduct, transparent communication, strong corporate social responsibility.

    ### Interdependencies:
    It's important to note that these risk types are often interconnected. For example, an operational failure (Operational Risk) could lead to significant financial losses (Credit/Market Risk) and severely damage a firm's standing (Reputational Risk). Effective risk management requires a holistic view, understanding these interdependencies, and developing integrated strategies.

    $$\text{Total Risk} = f(\text{Credit Risk}, \text{Market Risk}, \text{Operational Risk}, ...)$$

    The sum of all risks is not necessarily a simple addition due to diversification and correlation effects, often expressed as a non-linear function $f$.
    \"\"\"
    )
