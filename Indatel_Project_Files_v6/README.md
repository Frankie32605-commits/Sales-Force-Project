# INDATEL Pricing Intelligence Prototype

## Overview
This project is a standalone web application prototype built for INDATEL to analyze historical provider pricing and generate budgetary MRC/NRC estimates based on sanitized quoting data.

## Features
*   **Batch Quote Upload:** Upload a standard Excel RFQ/RFP sheet to process multiple sites simultaneously.
*   **Single Site Lookup:** Search historical records for specific ZIP codes and product parameters.
*   **Proximity & Match Quality Engine:** Results are categorized into 🟢 GREEN (Strong/Recent), 🟠 ORANGE (Review Required/Probable Match), and 🔴 RED (No Match) based on historical accuracy and recency.
*   **Priority Match Display:** Renders the exact underlying historical records used to calculate the budgetary estimates.
*   **Stop/Reset:** Interactively stop execution or clear the workspace.

## Requirements
*   Python 3.8+
*   Streamlit
*   Pandas (v2.1.0+ compatible)
*   Openpyxl

## Setup Instructions
1. Extract this folder.
2. Open the folder in VS Code or your preferred IDE.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
5. Access the dashboard via your local web browser.
