import streamlit as st
import plotly.graph_objects as go

from utils import (
    load_data,
    apply_filters,
    build_product_kpi,
    build_pareto
)


# ============================================================
# TITLE
# ============================================================

st.title("📈 Profit Concentration Analysis")

st.markdown(
    """
    Analyze how concentrated Nassau Candy's revenue and
    profit are across its product portfolio.
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
# PARETO TABLES
# ============================================================

revenue_pareto = build_pareto(
    product_kpi,
    "Total_Sales"
)

profit_pareto = build_pareto(
    product_kpi,
    "Total_Gross_Profit"
)


# ============================================================
# DEPENDENCY CALCULATIONS
# ============================================================

revenue_80 = (
    revenue_pareto[
        revenue_pareto["Cumulative %"] < 80
    ].shape[0]
    + 1
)

profit_80 = (
    profit_pareto[
        profit_pareto["Cumulative %"] < 80
    ].shape[0]
    + 1
)

total_products = len(product_kpi)

revenue_80_pct = (
    revenue_80 / total_products * 100
    if total_products
    else 0
)

profit_80_pct = (
    profit_80 / total_products * 100
    if total_products
    else 0
)


# ============================================================
# DEPENDENCY INDICATORS
# ============================================================

st.subheader("Dependency Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Products",
    total_products
)

col2.metric(
    "Products for 80% Revenue",
    revenue_80
)

col3.metric(
    "Products for 80% Profit",
    profit_80
)

col4.metric(
    "Profit Concentration",
    f"{profit_80_pct:.2f}% of products"
)


st.markdown("---")


# ============================================================
# REVENUE PARETO
# ============================================================

st.subheader("Revenue Pareto Analysis")

fig = go.Figure()

fig.add_bar(
    x=revenue_pareto["Product Name"],
    y=revenue_pareto["Total_Sales"],
    name="Sales"
)

fig.add_scatter(
    x=revenue_pareto["Product Name"],
    y=revenue_pareto["Cumulative %"],
    name="Cumulative Revenue %",
    yaxis="y2",
    mode="lines+markers"
)

fig.add_hline(
    y=80,
    line_dash="dash",
    yref="y2",
    annotation_text="80% Revenue"
)

fig.update_layout(
    title="Revenue Concentration — Pareto Analysis",
    xaxis_title="Product",
    yaxis_title="Sales",
    yaxis2=dict(
        title="Cumulative Revenue (%)",
        overlaying="y",
        side="right",
        range=[0, 105]
    ),
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# PROFIT PARETO
# ============================================================

st.subheader("Profit Pareto Analysis")

fig = go.Figure()

fig.add_bar(
    x=profit_pareto["Product Name"],
    y=profit_pareto["Total_Gross_Profit"],
    name="Gross Profit"
)

fig.add_scatter(
    x=profit_pareto["Product Name"],
    y=profit_pareto["Cumulative %"],
    name="Cumulative Profit %",
    yaxis="y2",
    mode="lines+markers"
)

fig.add_hline(
    y=80,
    line_dash="dash",
    yref="y2",
    annotation_text="80% Profit"
)

fig.update_layout(
    title="Profit Concentration — Pareto Analysis",
    xaxis_title="Product",
    yaxis_title="Gross Profit",
    yaxis2=dict(
        title="Cumulative Profit (%)",
        overlaying="y",
        side="right",
        range=[0, 105]
    ),
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# TOP PRODUCTS
# ============================================================

st.subheader("Products Driving Profit")

st.dataframe(
    profit_pareto[
        [
            "Product Name",
            "Division",
            "Total_Sales",
            "Total_Gross_Profit",
            "Profit Contribution %",
            "Cumulative %"
        ]
    ].head(10),
    use_container_width=True,
    hide_index=True
)