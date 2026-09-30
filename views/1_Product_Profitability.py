import streamlit as st
import plotly.express as px

from utils import (
    load_data,
    apply_filters,
    build_product_kpi,
    build_margin_volatility,
    format_currency
)


# ============================================================
# TITLE
# ============================================================

st.title("📊 Product Profitability Overview")

st.markdown(
    """
    Analyze product-level revenue, gross profit, margin,
    contribution and profitability risk.
    """
)


# ============================================================
# DATA
# ============================================================

df = load_data()
filtered_df = apply_filters(df)

product_kpi = build_product_kpi(filtered_df)


if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()


# ============================================================
# KPI CARDS
# ============================================================

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()
total_units = filtered_df["Units"].sum()

gross_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    format_currency(total_sales)
)

col2.metric(
    "Gross Profit",
    format_currency(total_profit)
)

col3.metric(
    "Gross Margin",
    f"{gross_margin:.2f}%"
)

col4.metric(
    "Total Units",
    f"{total_units:,}"
)


st.markdown("---")


# ============================================================
# PRODUCT PROFITABILITY CHARTS
# ============================================================

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Top 10 by Gross Profit
# ------------------------------------------------------------

with col1:

    top_profit = (
        product_kpi
        .sort_values(
            "Total_Gross_Profit",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top_profit.sort_values(
            "Total_Gross_Profit"
        ),
        x="Total_Gross_Profit",
        y="Product Name",
        orientation="h",
        title="Top 10 Products by Gross Profit",
        labels={
            "Total_Gross_Profit": "Gross Profit"
        }
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ------------------------------------------------------------
# Profit Contribution
# ------------------------------------------------------------

with col2:

    top_contribution = (
        product_kpi
        .sort_values(
            "Profit Contribution %",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top_contribution.sort_values(
            "Profit Contribution %"
        ),
        x="Profit Contribution %",
        y="Product Name",
        orientation="h",
        title="Top 10 Products by Profit Contribution",
        labels={
            "Profit Contribution %":
            "Profit Contribution (%)"
        }
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# MARGIN LEADERBOARD
# ============================================================

st.subheader("Product-Level Margin Leaderboard")

top_margin = (
    product_kpi
    .sort_values(
        "Gross Margin %",
        ascending=False
    )
    .head(10)
    .copy()
)

st.dataframe(
    top_margin[
        [
            "Product Name",
            "Division",
            "Total_Sales",
            "Total_Gross_Profit",
            "Gross Margin %",
            "Profit per Unit"
        ]
    ].rename(
        columns={
            "Product Name": "Product",
            "Total_Sales": "Sales",
            "Total_Gross_Profit": "Gross Profit"
        }
    ),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# PRODUCT PROFITABILITY TABLE
# ============================================================

st.subheader("Complete Product Profitability Analysis")

display_df = (
    product_kpi
    .sort_values(
        "Total_Gross_Profit",
        ascending=False
    )
    .copy()
)

st.dataframe(
    display_df[
        [
            "Product Name",
            "Division",
            "Total_Sales",
            "Total_Units",
            "Total_Cost",
            "Total_Gross_Profit",
            "Gross Margin %",
            "Profit per Unit",
            "Revenue Contribution %",
            "Profit Contribution %",
            "Cost % of Sales",
            "Margin Risk"
        ]
    ].rename(
        columns={
            "Product Name": "Product",
            "Total_Sales": "Sales",
            "Total_Units": "Units",
            "Total_Cost": "Cost",
            "Total_Gross_Profit": "Gross Profit"
        }
    ),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# MARGIN VOLATILITY
# ============================================================

with st.expander("Product Margin Volatility"):

    volatility = build_margin_volatility(
        filtered_df
    )

    if not volatility.empty:

        st.dataframe(
            volatility
            .sort_values(
                "Margin Volatility",
                ascending=False
            )
            .head(15),
            use_container_width=True,
            hide_index=True
        )