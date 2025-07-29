# Influencer Campaign Performance Dashboard

An interactive dashboard built using **Streamlit** to analyze influencer marketing campaign performance across platforms and products. This tool allows marketers and analysts to track KPIs, visualize revenue and ROAS trends, and generate downloadable campaign reports.

---

## Project Overview

This dashboard enables data-driven insights into influencer campaigns by offering:

- Key Performance Indicators (KPIs) like Total Revenue, Total Payout, and ROAS
- Dynamic filtering by platform, product, and influencer
- Visualizations to track top performers and platform revenue
- Upload support for custom campaign datasets
- CSV and PDF export options for filtered data

---

## Tech Stack

- **Python 3.9+**
- **Streamlit** (Frontend + Dashboard Engine)
- **Pandas** (Data Handling)
- **Plotly Express** (Visualizations)
- **FPDF** (PDF Export)
- **AgGrid (Optional)** for searchable tables
- **Custom CSS** for styling

---
##Setup Instructions

### 1. Clone the Repository

git clone https://github.com/BNaveenKumar325/Influencer-Campaign-Performance-Dashboard.git

cd influencer-dashboard
### 2. Create and Activate a Virtual Environment (Optional but Recommended)
# Windows
python -m venv env
env\Scripts\activate

# Mac/Linux
python3 -m venv env
source env/bin/activate

### 3. Install Dependencies

"pip install -r requirements.txt"

### 4. Run the Application

"streamlit run app.py"

The dashboard will automatically open in your default web browser.

