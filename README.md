# Nassau Candy Distributor
## Product Profitability & Margin Risk Analysis Dashboard

### Project Overview

This project analyzes Nassau Candy Distributor's sales, cost, gross profit, product margins, division performance, and profit concentration.

The main objective is to identify:
- Which products drive the most gross profit and margin
- Whether high-sales products are also profitable
- How profitability varies across divisions
- Which products create margin risk
- How concentrated revenue and profit are across the product portfolio

The project combines SQL, Python/Jupyter Notebook analysis, and an interactive Streamlit dashboard.

---

## Business Problem

Sales volume alone can be misleading. A product may have high sales but generate relatively low profit because of its cost structure.

The analysis therefore focuses on product-level profitability rather than sales alone, using metrics such as:
- Gross Margin %
- Gross Profit
- Profit per Unit
- Revenue Contribution %
- Profit Contribution %
- Cost % of Sales
- Margin Risk
- Margin Volatility

---

## Dataset Overview

The final analytical dataset contains:
- 9,994 transaction records
- 15 unique products
- 5,009 customers
- 8,389 orders
- 531 cities
- 49 states
- 3 product divisions
- 4 regions

Core financial fields:
- Sales
- Units
- Cost
- Gross Profit

Gross Profit is defined as:

`Gross Profit = Sales - Cost`

---

## Project Workflow

```text
SQL Database
     ↓
Data Extraction
     ↓
Data Cleaning & Validation
     ↓
Feature / KPI Engineering
     ↓
Exploratory Data Analysis
     ↓
Advanced Business Analysis
     ↓
Business Insights & Recommendations
     ↓
Streamlit Dashboard
```

---

## Analysis Performed

### 1. Data Cleaning & Validation
- Corrected date formats
- Converted Order Date and Ship Date to datetime
- Treated Customer ID and Postal Code as identifiers
- Checked missing values
- Checked duplicate records
- Validated profit calculations
- Validated date consistency
- Checked numerical values and business rules

### 2. Feature / KPI Engineering
- Gross Margin %
- Profit per Unit
- Shipping Days
- Order Year
- Order Month
- Order Month Name
- Year-Month
- Revenue Contribution %
- Profit Contribution %

### 3. Exploratory Data Analysis
- Overall sales, cost and profit performance
- Product-level sales and profitability
- Division performance
- Regional analysis
- State-level analysis
- Time-series analysis
- Shipping analysis

### 4. Advanced Business Analysis
- Product profitability segmentation
- Revenue Pareto analysis
- Profit Pareto analysis
- Profit concentration / dependency
- Cost vs margin diagnostics
- Margin-risk identification
- High-cost / low-margin analysis
- Division efficiency
- Margin volatility

---

## Key Business Findings

### Overall Performance

- Total Sales: $138,830.34
- Total Cost: $47,322.11
- Total Gross Profit: $91,508.23
- Total Units: 37,873
- Overall Gross Margin: 65.91%

### Product Concentration

Five Chocolate products represent one-third of the product portfolio but generate approximately:
- 92.93% of total revenue
- 95.11% of total gross profit

This indicates significant dependency on a small group of core products.

### Division Performance

Chocolate:
- Revenue: $129,019.61
- Gross Profit: $87,030.05
- Gross Margin: 67.45%
- Revenue Contribution: 92.93%
- Profit Contribution: 95.11%

Other:
- Revenue: $9,383.25
- Gross Profit: $4,193.45
- Gross Margin: 44.69%
- Revenue Contribution: 6.76%
- Profit Contribution: 4.58%

Sugar:
- Revenue: $427.48
- Gross Profit: $284.73
- Gross Margin: 66.61%

### Major Margin-Risk Product

Kazookles:
- Sales: $1,205.75
- Cost: $1,113.00
- Gross Profit: $92.75
- Gross Margin: 7.69%
- Cost as % of Sales: 92.31%

This makes Kazookles the strongest individual candidate for detailed pricing and cost investigation.

---

## Business Recommendations

1. Protect the five core Chocolate products because they currently generate the majority of company revenue and profit.

2. Conduct a detailed pricing and cost review for Kazookles because of its extremely low gross margin and high cost-to-sales ratio.

3. Review the Other division for margin improvement because its share of profit is lower than its share of revenue.

4. Optimize products such as Lickable Wallpaper and Wonka Gum through pricing, sourcing, or cost-efficiency review rather than automatically discontinuing them.

5. Evaluate whether high-margin, low-sales Sugar products have realistic growth potential.

6. Monitor dependency on the five core Chocolate products and gradually develop additional scalable products with healthy margins.

7. Use a multi-metric product monitoring framework covering sales, gross profit, gross margin, profit per unit, contribution, and margin risk.

8. Monitor monthly gross margin to detect meaningful deviations from the historical baseline.

---

## Streamlit Dashboard

The dashboard contains four main modules:

### Product Profitability Overview
- Product-level margin leaderboard
- Top products by gross profit
- Profit contribution charts
- Product profitability table
- Margin volatility view

### Division Performance Dashboard
- Revenue vs gross profit
- Gross margin by division
- Margin distribution by division
- Revenue vs profit contribution comparison

### Cost & Margin Diagnostics
- Cost vs sales scatter plot
- Sales vs gross margin analysis
- Margin risk flags
- High-cost / low-margin product identification

### Profit Concentration Analysis
- Revenue Pareto chart
- Profit Pareto chart
- 80% revenue dependency indicator
- 80% profit dependency indicator
- Products driving profit

---

## Interactive Dashboard Features

- Date range selector
- Division filter
- Product search
- Margin-risk threshold slider

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Plotly
- SQL / MySQL
- Jupyter Notebook
- Streamlit
- GitHub

---

## Project Structure

```text
Nassau_Candy_Dashboard/
│
├── app.py
├── utils.py
├── requirements.txt
├── README.md
│
├── data/
│   └── nassau_candy_analysis.csv
│
└── views/
    ├── 1_Product_Profitability.py
    ├── 2_Division_Performance.py
    ├── 3_Cost_Margin_Diagnostics.py
    └── 4_Profit_Concentration.py
```

---

## Run the Dashboard Locally

### 1. Create and activate the virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Streamlit application

```bash
streamlit run app.py
```

The dashboard will open in your web browser.

---

## Live Dashboard

Add your deployed Streamlit URL here:

**Live Dashboard:** `YOUR_STREAMLIT_APP_URL`

Example:

`https://your-app-name.streamlit.app`

---

## GitHub Repository

Add your GitHub repository link here:

**GitHub:** `YOUR_GITHUB_REPOSITORY_URL`

---

## Project Deliverables

- Jupyter Notebook: data cleaning, validation, EDA, advanced analysis and business recommendations
- Streamlit Dashboard: interactive profitability and margin-risk analytics
- GitHub Repository: source code and project files
- Project Report: findings, root-cause analysis and recommendations

---

## Note on Shipping Analysis

Shipping analysis was explored using Order Date, Ship Date and Shipping Days. Because the resulting shipping-duration values required further source-level validation, shipping metrics were not used as a primary basis for the profitability recommendations.

The primary project scope remains product profitability, division performance, cost structure and profit concentration.
