import streamlit as st
import plotly.express as px

from utils import (
    load_data,
    apply_filters,
    build_product_kpi
)


# ============================================================
# TITLE
# ============================================================

st.title("⚠️ Cost & Margin Diagnostics")

st.markdown(
    """
    Identify cost-heavy products, low-margin products
    and potential margin-risk areas.
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
# COST VS SALES
# ============================================================

st.subheader("Cost vs Sales")

fig = px.scatter(
    product_kpi,
    x="Total_Sales",
    y="Total_Cost",
    size="Total_Gross_Profit",
    color="Division",
    hover_name="Product Name",
    hover_data=[
        "Gross Margin %",
        "Profit per Unit",
        "Cost % of Sales"
    ],
    title="Product Cost vs Sales",
    labels={
        "Total_Sales": "Sales",
        "Total_Cost": "Cost"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# SALES VS MARGIN
# ============================================================

st.subheader("Sales vs Gross Margin")

sales_median = product_kpi[
    "Total_Sales"
].median()

margin_threshold = st.session_state.get(
    "margin_threshold",
    50.0
)

fig = px.scatter(
    product_kpi,
    x="Total_Sales",
    y="Gross Margin %",
    size="Total_Gross_Profit",
    color="Division",
    hover_name="Product Name",
    hover_data=[
        "Total_Gross_Profit",
        "Cost % of Sales",
        "Profit per Unit"
    ],
    title="Product Sales vs Gross Margin",
    labels={
        "Total_Sales": "Sales",
        "Gross Margin %":
        "Gross Margin (%)"
    }
)

fig.add_hline(
    y=margin_threshold,
    line_dash="dash",
    annotation_text=(
        f"Margin Threshold: "
        f"{margin_threshold:.1f}%"
    )
)

fig.add_vline(
    x=sales_median,
    line_dash="dash",
    annotation_text="Median Sales"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# MARGIN RISK FLAGS
# ============================================================

st.subheader("Margin Risk Flags")

risk_df = (
    product_kpi[
        product_kpi["Margin Risk"] != "Normal"
    ]
    .sort_values(
        [
            "Margin Risk",
            "Gross Margin %"
        ]
    )
)

if risk_df.empty:

    st.success(
        "No products meet the current margin-risk criteria."
    )

else:

    st.dataframe(
        risk_df[
            [
                "Product Name",
                "Division",
                "Total_Sales",
                "Total_Cost",
                "Total_Gross_Profit",
                "Gross Margin %",
                "Cost % of Sales",
                "Profit per Unit",
                "Margin Risk"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# HIGH COST + LOW MARGIN
# ============================================================

st.subheader("High Cost + Low Margin Products")

cost_threshold = product_kpi[
    "Total_Cost"
].median()

high_cost_low_margin = product_kpi[
    (
        product_kpi["Total_Cost"]
        >= cost_threshold
    )
    &
    (
        product_kpi["Gross Margin %"]
        <= margin_threshold
    )
].sort_values(
    "Total_Cost",
    ascending=False
)

st.dataframe(
    high_cost_low_margin[
        [
            "Product Name",
            "Division",
            "Total_Sales",
            "Total_Cost",
            "Total_Gross_Profit",
            "Gross Margin %",
            "Cost % of Sales"
        ]
    ],
    use_container_width=True,
    hide_index=True
)