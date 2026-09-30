import streamlit as st

from utils import load_data


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nassau Candy Profitability Dashboard",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()


# ============================================================
# NAVIGATION
# ============================================================

pg = st.navigation(
    [
        st.Page(
            "views/1_Product_Profitability.py",
            title="Product Profitability",
            icon="📊"
        ),

        st.Page(
            "views/2_Division_Performance.py",
            title="Division Performance",
            icon="🏢"
        ),

        st.Page(
            "views/3_Cost_Margin_Diagnostics.py",
            title="Cost & Margin Diagnostics",
            icon="⚠️"
        ),

        st.Page(
            "views/4_Profit_Concentration.py",
            title="Profit Concentration",
            icon="📈"
        )
    ],
    position="sidebar"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Nassau Candy")
st.sidebar.caption(
    "Product Profitability & Margin Analytics"
)

st.sidebar.markdown("---")

st.sidebar.subheader("Dashboard Filters")


# ------------------------------------------------------------
# Date Range
# ------------------------------------------------------------

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="date_range"
)


# ------------------------------------------------------------
# Division Filter
# ------------------------------------------------------------

divisions = sorted(
    df["Division"]
    .dropna()
    .unique()
    .tolist()
)

st.sidebar.multiselect(
    "Division",
    options=divisions,
    default=divisions,
    key="division_filter"
)


# ------------------------------------------------------------
# Product Search
# ------------------------------------------------------------

st.sidebar.text_input(
    "Product Search",
    placeholder="Search product name...",
    key="product_search"
)


# ------------------------------------------------------------
# Margin Threshold
# ------------------------------------------------------------

st.sidebar.slider(
    "Margin Risk Threshold (%)",
    min_value=0.0,
    max_value=100.0,
    value=50.0,
    step=1.0,
    key="margin_threshold",
    help=(
        "Products at or below this gross margin "
        "are considered margin-risk candidates."
    )
)


st.sidebar.markdown("---")

st.sidebar.caption(
    f"Data coverage: {min_date} → {max_date}"
)

st.sidebar.caption(
    f"Source records: {len(df):,}"
)


# ============================================================
# RUN SELECTED PAGE
# ============================================================

pg.run()