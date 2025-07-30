
# QuLab: Risk Appetite & Allocation Modeler


## 1. Project Title and Description

**QuLab** is an interactive Streamlit application designed for a lab project to explore the core concepts of **Risk Appetite and Allocation** within an organizational context. It provides a visual and interactive platform to define, distribute, and monitor risk limits across various business units, aggregating individual risk exposures to assess overall firm health against strategic objectives.

This application serves as an educational tool to understand:
*   The hierarchical breakdown of a firm's `Board Appetite`.
*   The process of cascading `Allocated Appetite` to individual business units.
*   The aggregation of `Individual Risk Exposures` to form a `Total Firm Risk Profile`.
*   The comparison of aggregated risk against defined limits using a intuitive Red, Amber, Green (RAG) status system.

### Key Concepts Explored:
*   **Board Appetite:** The maximum level of risk a firm is willing to accept to achieve its strategic objectives.
*   **Allocated Appetite:** The portion of the Board Appetite assigned to specific business units or functions.
*   **Individual Risk Exposure:** The actual or estimated risk a specific business unit is facing (e.g., operational losses, credit exposure).
*   **Risk Tolerance:** The acceptable deviation from the allocated appetite before triggering management action. It is expressed as a factor that, when multiplied by Allocated Appetite, gives Absolute Risk Tolerance.
*   **Risk Status (RAG):**
    *   `Green`: Exposure $\le$ Allocated Appetite
    *   `Amber`: Allocated Appetite $<$ Exposure $\le$ Absolute Risk Tolerance
    *   `Red`: Exposure $>$ Absolute Risk Tolerance

## 2. Features

The QuLab application offers the following key functionalities:

*   **Interactive Board Appetite Definition:** Easily set the firm's top-level risk appetite using a slider.
*   **Dynamic Appetite Allocation:** Distribute the Board Appetite among predefined business units through interactive percentage inputs. Includes real-time validation to ensure allocations sum to 100%.
*   **Synthetic Data Generation:** Automatically generates simulated individual risk exposures and risk tolerance factors for business units to kickstart analysis.
*   **Risk Exposure Overrides:** Allows users to manually override the simulated individual risk exposures for each business unit with actual or hypothetical values.
*   **Automated Risk Status Assessment (RAG Logic):** Calculates and displays the risk status (Green, Amber, Red) for each business unit based on its exposure relative to its allocated appetite and absolute risk tolerance.
*   **Comprehensive Summary Table:** Presents a clear tabular overview of each business unit's allocated appetite, individual risk exposure, absolute risk tolerance, and current risk status.
*   **Business Unit Risk Comparison Chart:** Visualizes individual business unit risk exposures against their allocated appetite and absolute risk tolerance using an interactive bar chart (Plotly Express).
*   **Hierarchical Risk Allocation Treemap:** Provides a visual representation of the hierarchical breakdown of risk appetite, showing the firm's total appetite and how it's distributed among business units.
*   **Overall Firm Risk Profile Summary:** Aggregates individual risk exposures to present the total firm risk, comparing it directly against the Board Appetite with a clear status message.
*   **Multi-Page Navigation:** Includes placeholder pages (`Page 2: Additional Analysis` and `Page 3: Resources & Glossary`) for future enhancements and provides relevant definitions and external resources.

## 3. Getting Started

Follow these instructions to set up and run the application on your local machine.

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-qu-lab-project.git
    cd your-qu-lab-project
    ```
    (Replace `your-username/your-qu-lab-project` with the actual repository URL)

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    Create a `requirements.txt` file in the root directory of your project with the following content:
    ```
    streamlit
    pandas
    numpy
    plotly
    ```
    Then, install them:
    ```bash
    pip install -r requirements.txt
    ```

## 4. Usage

To run the Streamlit application:

1.  **Navigate to the project root directory** (where `app.py` is located) in your terminal.
2.  **Ensure your virtual environment is activated.**
3.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

    This command will open the application in your default web browser (usually at `http://localhost:8501`).

### Basic Usage Instructions:

1.  **`app.py` (Main Page):**
    *   The initial page provides an overview of the application and the key concepts of Risk Appetite and Allocation.
    *   Use the sidebar on the left to navigate between pages: "Risk Appetite Modeler", "Page 2", and "Page 3".

2.  **`Risk Appetite Modeler` Page:**
    *   **Define Parameters:**
        *   Adjust the **"Board Appetite ($ Millions)"** slider to set the firm's total risk capacity.
        *   Modify the **"Allocation Percentages (%)"** for each business unit. Ensure the sum of percentages is exactly 100% to proceed with calculations.
    *   **Individual Risk Exposure Overrides (Optional):**
        *   The application generates synthetic data for individual business unit exposures. You can view these or override them with your own values in this section.
    *   **Observe Results:**
        *   The **"Summary of Risk Allocation & Status"** table will update dynamically, showing allocated appetite, actual exposure, tolerance, and the RAG status for each unit.
        *   The **"Business Unit Risk Exposure vs. Appetite & Tolerance"** bar chart visually compares these metrics.
        *   The **"Hierarchical Risk Appetite Allocation"** treemap shows the breakdown of the total appetite.
        *   The **"Overall Firm Risk Profile Summary"** provides a crucial comparison of the aggregated total firm risk against the Board Appetite.

3.  **`Page 2: Additional Analysis` and `Page 3: Resources & Glossary`:**
    *   These pages provide placeholders for future enhancements and useful definitions/resources related to risk management.

## 5. Project Structure

The project is organized into the following directories and files:

```
qu-lab-project/
├── app.py
├── application_pages/
│   ├── __init__.py
│   ├── page1.py
│   ├── page2.py
│   └── page3.py
├── requirements.txt
└── README.md
```

*   `app.py`: The main Streamlit application entry point. Handles overall layout, navigation, and initial description.
*   `application_pages/`: A directory containing individual Python modules for each distinct page of the Streamlit application.
    *   `page1.py`: Contains the core logic and UI for the "Risk Appetite Modeler" page, including data generation, calculations, and visualizations.
    *   `page2.py`: A placeholder page for future feature development (e.g., historical analysis, scenario testing).
    *   `page3.py`: A page providing a glossary of terms and additional resources related to risk management.
*   `requirements.txt`: Lists all Python dependencies required to run the application.
*   `README.md`: This file, providing project information and instructions.

## 6. Technology Stack

*   **Framework:** [Streamlit](https://streamlit.io/)
*   **Programming Language:** Python
*   **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
*   **Numerical Operations:** [NumPy](https://numpy.org/)
*   **Interactive Visualizations:** [Plotly Express](https://plotly.com/python/plotly-express/)

## 7. Contributing

This project is primarily a lab exercise. However, if you have suggestions for improvements or bug fixes, feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/AmazingFeature` or `fix/BugFix`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
5.  Push to the branch (`git push origin feature/AmazingFeature`).
6.  Open a Pull Request.

## 8. License

This project is licensed under the MIT License - see the `LICENSE` file (if applicable, otherwise state it's for educational purposes and not for commercial distribution without explicit permission). For lab projects, it's common to implicitly grant educational use.

## 9. Contact

For any questions or further information, please reach out via the GitHub issues page of this repository.

---
**QuantUniversity**
_Empowering financial professionals with quantitative skills._

## License

## QuantUniversity License

© QuantUniversity 2025  
This notebook was created for **educational purposes only** and is **not intended for commercial use**.  

- You **may not copy, share, or redistribute** this notebook **without explicit permission** from QuantUniversity.  
- You **may not delete or modify this license cell** without authorization.  
- This notebook was generated using **QuCreate**, an AI-powered assistant.  
- Content generated by AI may contain **hallucinated or incorrect information**. Please **verify before using**.  

All rights reserved. For permissions or commercial licensing, contact: [info@qusandbox.com](mailto:info@qusandbox.com)
