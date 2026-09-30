from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st


# ============================================================
# 1. DATA PATH
# ============================================================

DATA_PATH = (
    Path(__file__).resolve().parent
    / "data"
    / "nassau_candy_analysis.csv"
)


# ============================================================
# 2. LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    """
    Load the final cleaned and feature-engineered dataset.
    Streamlit caches the result so the CSV is not re-read
    unnecessarily on every interaction.
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    # --------------------------------------------------------
    # Data types
    # --------------------------------------------------------

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        errors="coerce"
    )

    df["Customer ID"] = df["Customer ID"].astype("string")
    df["Postal Code"] = df["Postal Code"].astype("string")

    # --------------------------------------------------------
    # Recalculate important features to make the app robust
    # --------------------------------------------------------

    df["Gross Margin %"] = np.where(
        df["Sales"] != 0,
        (df["Gross Profit"] / df["Sales"]) * 100,
        np.nan
    )

    df["Profit per Unit"] = np.where(
        df["Units"] != 0,
        df["Gross Profit"] / df["Units"],
        np.nan
    )

    df["Shipping Days"] = (
        df["Ship Date"] - df["Order Date"]
    ).dt.days

    df["Order Year"] = df["Order Date"].dt.year

    df["Order Month"] = df["Order Date"].dt.month

    df["Order Month Name"] = (
        df["Order Date"].dt.month_name()
    )

    df["Year-Month"] = (
        df["Order Date"]
        .dt.to_period("M")
        .astype(str)
    )

    return df


# ============================================================
# 3. APPLY GLOBAL FILTERS
# ============================================================

def apply_filters(df):
    """
    Apply date, division and product-search filters
    selected in the Streamlit sidebar.
    """

    filtered_df = df.copy()

    # --------------------------------------------------------
    # Date filter
    # --------------------------------------------------------

    date_range = st.session_state.get("date_range")

    if date_range and len(date_range) == 2:

        start_date, end_date = date_range

        filtered_df = filtered_df[
            (
                filtered_df["Order Date"].dt.date
                >= start_date
            )
            &
            (
                filtered_df["Order Date"].dt.date
                <= end_date
            )
        ]

    # --------------------------------------------------------
    # Division filter
    # --------------------------------------------------------

    selected_divisions = st.session_state.get(
        "division_filter",
        []
    )

    if selected_divisions:
        filtered_df = filtered_df[
            filtered_df["Division"].isin(
                selected_divisions
            )
        ]

    # --------------------------------------------------------
    # Product search
    # --------------------------------------------------------

    product_search = st.session_state.get(
        "product_search",
        ""
    ).strip()

    if product_search:

        filtered_df = filtered_df[
            filtered_df["Product Name"]
            .astype(str)
            .str.contains(
                product_search,
                case=False,
                na=False
            )
        ]

    return filtered_df.copy()


# ============================================================
# 4. PRODUCT KPI TABLE
# ============================================================

def build_product_kpi(df):

    if df.empty:
        return pd.DataFrame()

    product_kpi = (
        df.groupby(
            [
                "Product ID",
                "Product Name",
                "Division"
            ],
            as_index=False
        )
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Units=("Units", "sum"),
            Total_Cost=("Cost", "sum"),
            Total_Gross_Profit=("Gross Profit", "sum")
        )
    )

    product_kpi["Gross Margin %"] = np.where(
        product_kpi["Total_Sales"] != 0,
        (
            product_kpi["Total_Gross_Profit"]
            / product_kpi["Total_Sales"]
        ) * 100,
        np.nan
    )

    product_kpi["Profit per Unit"] = np.where(
        product_kpi["Total_Units"] != 0,
        (
            product_kpi["Total_Gross_Profit"]
            / product_kpi["Total_Units"]
        ),
        np.nan
    )

    total_sales = product_kpi["Total_Sales"].sum()

    total_profit = product_kpi[
        "Total_Gross_Profit"
    ].sum()

    product_kpi["Revenue Contribution %"] = np.where(
        total_sales != 0,
        (
            product_kpi["Total_Sales"]
            / total_sales
        ) * 100,
        np.nan
    )

    product_kpi["Profit Contribution %"] = np.where(
        total_profit != 0,
        (
            product_kpi["Total_Gross_Profit"]
            / total_profit
        ) * 100,
        np.nan
    )

    product_kpi["Cost % of Sales"] = np.where(
        product_kpi["Total_Sales"] != 0,
        (
            product_kpi["Total_Cost"]
            / product_kpi["Total_Sales"]
        ) * 100,
        np.nan
    )

    # --------------------------------------------------------
    # Margin threshold
    # --------------------------------------------------------

    margin_threshold = st.session_state.get(
        "margin_threshold",
        50.0
    )

    sales_median = product_kpi[
        "Total_Sales"
    ].median()

    product_kpi["Margin Risk"] = np.select(
        [
            (
                product_kpi["Gross Margin %"]
                <= margin_threshold
            )
            &
            (
                product_kpi["Cost % of Sales"]
                >= 80
            ),

            (
                product_kpi["Gross Margin %"]
                <= margin_threshold
            )
            &
            (
                product_kpi["Total_Sales"]
                >= sales_median
            ),

            product_kpi["Gross Margin %"]
            <= margin_threshold
        ],

        [
            "Critical",
            "High",
            "Monitor"
        ],

        default="Normal"
    )

    return product_kpi


# ============================================================
# 5. DIVISION KPI TABLE
# ============================================================

def build_division_kpi(df):

    if df.empty:
        return pd.DataFrame()

    division_kpi = (
        df.groupby(
            "Division",
            as_index=False
        )
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Units=("Units", "sum"),
            Total_Cost=("Cost", "sum"),
            Total_Gross_Profit=("Gross Profit", "sum")
        )
    )

    division_kpi["Gross Margin %"] = (
        division_kpi["Total_Gross_Profit"]
        / division_kpi["Total_Sales"]
    ) * 100

    division_kpi["Profit per Unit"] = (
        division_kpi["Total_Gross_Profit"]
        / division_kpi["Total_Units"]
    )

    total_sales = division_kpi["Total_Sales"].sum()

    total_profit = division_kpi[
        "Total_Gross_Profit"
    ].sum()

    division_kpi["Revenue Contribution %"] = (
        division_kpi["Total_Sales"]
        / total_sales
    ) * 100

    division_kpi["Profit Contribution %"] = (
        division_kpi["Total_Gross_Profit"]
        / total_profit
    ) * 100

    division_kpi["Revenue-Profit Gap %"] = (
        division_kpi["Revenue Contribution %"]
        - division_kpi["Profit Contribution %"]
    )

    return division_kpi


# ============================================================
# 6. MONTHLY KPI TABLE
# ============================================================

def build_monthly_kpi(df):

    if df.empty:
        return pd.DataFrame()

    monthly_kpi = (
        df.groupby(
            "Year-Month",
            as_index=False
        )
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Gross Profit", "sum"),
            Total_Units=("Units", "sum")
        )
    )

    monthly_kpi["Gross Margin %"] = (
        monthly_kpi["Total_Profit"]
        / monthly_kpi["Total_Sales"]
    ) * 100

    monthly_kpi["Month"] = pd.to_datetime(
        monthly_kpi["Year-Month"]
    )

    monthly_kpi = monthly_kpi.sort_values(
        "Month"
    )

    return monthly_kpi


# ============================================================
# 7. PARETO TABLE
# ============================================================

def build_pareto(product_kpi, metric):

    if product_kpi.empty:
        return pd.DataFrame()

    pareto = product_kpi.sort_values(
        metric,
        ascending=False
    ).copy()

    total_value = pareto[metric].sum()

    if total_value == 0:
        pareto["Contribution %"] = 0
    else:
        pareto["Contribution %"] = (
            pareto[metric]
            / total_value
        ) * 100

    pareto["Cumulative %"] = (
        pareto["Contribution %"]
        .cumsum()
    )

    return pareto


# ============================================================
# 8. MARGIN VOLATILITY
# ============================================================

def build_margin_volatility(df):

    if df.empty:
        return pd.DataFrame()

    monthly = (
        df.groupby(
            [
                "Product ID",
                "Product Name",
                "Year-Month"
            ],
            as_index=False
        )
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Gross Profit", "sum")
        )
    )

    monthly["Gross Margin %"] = np.where(
        monthly["Sales"] != 0,
        (
            monthly["Profit"]
            / monthly["Sales"]
        ) * 100,
        np.nan
    )

    volatility = (
        monthly.groupby(
            [
                "Product ID",
                "Product Name"
            ],
            as_index=False
        )["Gross Margin %"]
        .std()
        .rename(
            columns={
                "Gross Margin %":
                "Margin Volatility"
            }
        )
    )

    return volatility


# ============================================================
# 9. FORMAT CURRENCY
# ============================================================

def format_currency(value):
    return f"${value:,.2f}"


def format_percent(value):
    return f"{value:.2f}%"