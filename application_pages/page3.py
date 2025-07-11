
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm

def run_page3():
    st.title("Basic VaR (Value at Risk) Calculation")
    st.markdown(r\"\"\"
    **Value at Risk (VaR)** is a widely used financial risk management metric that estimates the potential loss of an investment or portfolio over a specified period for a given confidence level. It answers the question: "What is the maximum amount I could lose over a certain time horizon with a given probability?"

    ### Key Concepts of VaR:
    *   **Loss (or Gain):** The change in value of a portfolio over the time horizon.
    *   **Time Horizon:** The period over which the potential loss is estimated (e.g., 1 day, 10 days, 1 year).
    *   **Confidence Level:** The probability that the actual loss will not exceed the VaR estimate (e.g., 95%, 99%).

    ### Methods of VaR Calculation:

    1.  **Parametric VaR (Variance-Covariance Method):**
        This method assumes that portfolio returns are normally distributed. It calculates VaR using the mean and standard deviation of historical returns.

        Formula for a single asset:
        $$ \text{VaR}_{\alpha} = \mu - z_{\alpha} \times \sigma $$
        Where:
        *   $\mu$ is the expected (mean) return of the asset/portfolio.
        *   $\sigma$ is the standard deviation of the asset/portfolio returns.
        *   $z_{\alpha}$ is the Z-score corresponding to the desired confidence level $\alpha$ (e.g., for 95% confidence, $z_{0.05} \approx -1.645$ for losses; for 99% confidence, $z_{0.01} \approx -2.326$).
        *   For expressing VaR as a positive loss amount, we often use $|\text{VaR}_{\alpha}| = z_{\alpha} \times \sigma - \mu$. If $\mu$ is negligible or 0, then $\text{VaR}_{\alpha} \approx z_{\alpha} \times \sigma$.

        This method is simple but relies on the assumption of normal distribution, which may not hold true for all financial assets, especially during market turmoil.

    2.  **Historical VaR:**
        This method is non-parametric and relies on historical data to simulate future price movements. It involves ordering historical returns from worst to best and finding the return at the desired confidence level percentile.

        Example: To find 95% Historical VaR for a 1-day horizon, you would take the 5th percentile of the historical daily returns.

    3.  **Monte Carlo VaR:**
        This method involves generating many random scenarios for future market movements based on statistical models. For each scenario, the portfolio value is calculated, and then the VaR is determined from the distribution of these simulated portfolio values, similar to the Historical VaR method.

    ### Interactive VaR Calculator (Parametric Method)
    Let's calculate a simple Parametric VaR for a hypothetical portfolio.
    \"\"\"
    )

    st.divider()

    st.header("Parametric VaR Calculator")

    st.sidebar.header("VaR Parameters")
    portfolio_value = st.sidebar.number_input(
        "Portfolio Value ($)",
        min_value=1000.0,
        max_value=1_000_000_000.0,
        value=1_000_000.0,
        step=10000.0,
        help="Current market value of the investment portfolio."
    )

    daily_mean_return = st.sidebar.number_input(
        "Expected Daily Mean Return (%)",
        min_value=-5.0,
        max_value=5.0,
        value=0.05,
        step=0.01,
        format="%.2f",
        help="Average daily percentage return of the portfolio."
    ) / 100 # Convert to decimal

    daily_std_dev = st.sidebar.number_input(
        "Daily Standard Deviation of Returns (%)",
        min_value=0.1,
        max_value=10.0,
        value=1.5,
        step=0.1,
        format="%.1f",
        help="Volatility of the portfolio's daily returns."
    ) / 100 # Convert to decimal

    confidence_level = st.sidebar.slider(
        "Confidence Level (%)",
        min_value=90,
        max_value=99,
        value=95,
        step=1,
        help="The probability that the loss will not exceed the VaR estimate."
    ) / 100 # Convert to decimal

    time_horizon_days = st.sidebar.number_input(
        "Time Horizon (Days)",
        min_value=1,
        max_value=250,
        value=1,
        step=1,
        help="The number of days over which the VaR is calculated."
    )

    # Calculate Z-score
    # For a loss perspective, we want the left tail percentile
    z_score = norm.ppf(1 - confidence_level) # e.g., for 95%, 1-0.95 = 0.05. norm.ppf(0.05) gives -1.645

    # Scale mean and std dev for the time horizon
    # Assuming independent daily returns for scaling
    horizon_mean_return = daily_mean_return * time_horizon_days
    horizon_std_dev = daily_std_dev * np.sqrt(time_horizon_days)

    # Calculate VaR in percentage terms
    var_percent = (horizon_mean_return + z_score * horizon_std_dev)

    # Calculate VaR in monetary terms (as a positive loss)
    # The VaR is the negative of the calculated value, representing a loss
    var_monetary = - (var_percent * portfolio_value)

    st.subheader("Calculation Results")
    st.markdown(f"**Portfolio Value:** ${portfolio_value:,.2f}")
    st.markdown(f"**Time Horizon:** {time_horizon_days} day(s)")
    st.markdown(f"**Confidence Level:** {confidence_level*100:.0f}%")
    st.markdown(f"**Scaled Mean Return (over horizon):** {horizon_mean_return*100:.2f}%")
    st.markdown(f"**Scaled Standard Deviation (over horizon):** {horizon_std_dev*100:.2f}%")
    st.markdown(f"**Z-score (for {confidence_level*100:.0f}% confidence):** {z_score:.3f}")
    st.markdown(r"$$\text{VaR}_{\alpha} = \mu - z_{\alpha} \times \sigma$$")

    if var_monetary > 0:
        st.metric(
            label=f"Value at Risk (VaR) at {confidence_level*100:.0f}% Confidence",
            value=f"${var_monetary:,.2f}"
        )
        st.markdown(f"This means there is a **{100 - confidence_level*100:.0f}% chance** that the portfolio could lose **${var_monetary:,.2f} or more** over the next **{time_horizon_days} day(s)**.")
    else:
        st.metric(
            label=f"Value at Risk (VaR) at {confidence_level*100:.0f}% Confidence",
            value=f"No Loss (or expected gain of ${-var_monetary:,.2f})"
        )
        st.markdown(f"Based on the inputs, at a {confidence_level*100:.0f}% confidence level, the portfolio is not expected to incur a loss over {time_horizon_days} day(s), or is expected to gain ${-var_monetary:,.2f} or more.")


    st.subheader("Visualizing the Distribution")
    # Generate a range for the x-axis (returns)
    x = np.linspace(horizon_mean_return - 4 * horizon_std_dev, horizon_mean_return + 4 * horizon_std_dev, 1000)
    # Calculate the PDF for the normal distribution
    pdf = norm.pdf(x, horizon_mean_return, horizon_std_dev)

    fig_dist = go.Figure()
    fig_dist.add_trace(go.Scatter(x=x*portfolio_value, y=pdf, mode='lines', name='Return Distribution (Monetary)'))

    # Shade the VaR area
    x_fill = x[x <= var_percent]
    pdf_fill = pdf[x <= var_percent]
    fig_dist.add_trace(go.Scatter(x=x_fill*portfolio_value, y=pdf_fill, fill='tozeroy', mode='none',
                                  fillcolor='rgba(255, 0, 0, 0.3)', name='VaR Area (Loss)'))

    # Add VaR line
    fig_dist.add_vline(x=-var_monetary, line_dash="dash", line_color="red",
                       annotation_text=f"VaR: ${var_monetary:,.0f}",
                       annotation_position="top right")

    fig_dist.update_layout(
        title="Portfolio Return Distribution and VaR",
        xaxis_title="Portfolio Gain/Loss ($)",
        yaxis_title="Probability Density",
        hovermode="x unified",
        showlegend=True
    )
    st.plotly_chart(fig_dist, use_container_width=True)

    st.markdown(r\"\"\"
    ### Limitations of VaR:
    *   **Normal Distribution Assumption:** Parametric VaR assumes returns are normally distributed, which is often not true for financial assets (they exhibit fat tails, skewness).
    *   **Tail Risk:** VaR does not tell you the magnitude of losses beyond the VaR level. It only states the maximum loss up to a certain confidence level, not what happens in extreme events (this is where **Expected Shortfall** or **Conditional VaR** comes in).
    *   **Single Number:** It condenses complex risk into a single number, which can oversimplify the risk profile.
    *   **Historical Data Dependence:** Historical VaR is reliant on past market behavior, which may not be indicative of future behavior.

    Despite its limitations, VaR remains a cornerstone of risk management due to its simplicity and widespread acceptance for regulatory reporting and internal risk limits.
    \"\"\"
    )
