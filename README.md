# Quantifai Data Engineering Challenge

This repository contains my submission for the Quantifai Data & AI Engineering Internship (Take-Home Assignment). The goal of this project is to build an end-to-end ETL pipeline and interactive dashboard from messy e-commerce data.

## Problem Statement

You're a Data Engineering Intern at a fictional company that acquired multiple e-commerce platforms with inconsistent, messy datasets. Your mission:

- Clean and normalize raw data from various formats (CSV, JSON)
- Build an ETL pipeline to transform and load the data into a relational database
- Create a Streamlit dashboard to explore key business insights and metrics
- (Optional) Use AI techniques to reconcile schema differences

## Folder Structure

quantifai-project/
├── data/ # Raw datasets (JSON, CSV)
│ ├── customers_messy_data.json
│ ├── products_inconsistent_data.json
│ └── orders_unstructured_data.csv
│
├── database/
│ └── quantifai.db # SQLite database with cleaned data
│
├── notebooks/
│ └── data_cleaning.ipynb # Jupyter notebook with data exploration + logic
│
├── scripts/ # Data transformation logic
│ ├── transform_customer.py
│ ├── transform_order.py
│ └── transform_product.py
│
├── streamlit_app/
│ └── app.py # Interactive dashboard
│
├── load_to_sqlite.py # Script to load cleaned data into SQLite
├── requirements.txt # Required libraries
└── README.md


## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/quantifai-project.git
   cd quantifai-project
2. Install Dependencies
pip install -r requirements.txt

3. Run The Pipeline 
python load_to_sqlite.py

4. Launch The Dashboard
streamlit run streamlit_app/app.py


Features => 

Complete ETL process using Python and Pandas
Data cleaning with handling of inconsistencies, nulls, and format mismatches
Normalized schema stored in SQLite
Interactive Streamlit dashboard for:
Customer search, filter, and segment analysis
Orders summary and metrics
Product overview and order trends
Segment and gender visualizations
Data export as CSV


Requirements => 

pandas
numpy
streamlit
plotly


Install with
pip install -r requirements.txt
