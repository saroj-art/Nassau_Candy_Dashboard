import streamlit as st
import plotly.express as px

from utils import (
    load_data,
    apply_filters,
    build_division_kpi,
    format_currency
)


# ============================================================
# TITLE
# ============================================================

st.title("🏢 Division Performance Dashboard")

st.markdown(
    """
    Compare revenue, gross profit and margin performance
    across product divisions.
    """
)


# ============================================================
# DATA
# ============================================================

df = load_data()
filtered_df = apply_filters(df)

division_kpi = build_division_kpi(filtered_df)


if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()


# ============================================================
# KPI CARDS
# ============================================================

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()

gross_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Revenue",
    format_currency(total_sales)
)

col2.metric(
    "Total Gross Profit",
    format_currency(total_profit)
)

col3.metric(
    "Overall Gross Margin",
    f"{gross_margin:.2f}%"
)


st.markdown("---")


# ============================================================
# REVENUE VS PROFIT
# ============================================================

fig = px.scatter(
    division_kpi,
    x="Total_Sales",
    y="Total_Gross_Profit",
    size="Total_Sales",
    color="Division",
    text="Division",
    title="Revenue vs Gross Profit by Division",
    labels={
        "Total_Sales": "Revenue",
        "Total_Gross_Profit": "Gross Profit"
    }
)

fig.update_traces(
    textposition="top center"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# MARGIN BY DIVISION
# ============================================================

fig = px.bar(
    division_kpi.sort_values(
        "Gross Margin %"
    ),
    x="Division",
    y="Gross Margin %",
    title="Gross Margin by Division",
    text="Gross Margin %",
    labels={
        "Gross Margin %":
        "Gross Margin (%)"
    }
)

fig.update_traces(
    texttemplate="%{text:.2f}%"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# MARGIN DISTRIBUTION
# ============================================================

st.subheader("Margin Distribution by Division")

fig = px.box(
    filtered_df,
    x="Division",
    y="Gross Margin %",
    color="Division",
    points="outliers",
    title="Gross Margin Distribution by Division"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# DIVISION PERFORMANCE TABLE
# ============================================================

st.subheader("Division Performance Summary")

st.dataframe(
    division_kpi[
        [
            "Division",
            "Total_Sales",
            "Total_Profit",
            "Gross Margin %",
            "Revenue Contribution %",
            "Profit Contribution %",
            "Revenue-Profit Gap %"
        ]
    ].sort_values(
        "Total_Profit",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)