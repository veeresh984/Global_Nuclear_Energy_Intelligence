import streamlit as st
import pandas as pd

from utils.data_loader import (
    load_data,
    get_country_list
)

from utils.analytics import (
    get_country_data,
    country_nuclear_growth,
    renewable_growth
)

from utils.charts import (
    line_chart,
    multi_line_chart,
    country_comparison_chart,
    bubble_chart
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Country Analysis",
    page_icon="🏭",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

countries = get_country_list(df)

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Country Filters")

selected_country = st.sidebar.selectbox(
    "Select Country",
    countries
)

comparison_countries = st.sidebar.multiselect(
    "Compare With",
    countries,
    default=[selected_country]
)

# =====================================================
# COUNTRY DATA
# =====================================================

country_df = get_country_data(
    df,
    selected_country
)

latest_record = country_df.iloc[-1]

# =====================================================
# HEADER
# =====================================================

st.title(f"🏭 {selected_country}")

st.markdown(
    """
    Comprehensive country-level energy intelligence,
    sustainability analytics,
    emissions monitoring,
    and nuclear performance evaluation.
    """
)

st.divider()

# =====================================================
# KPI SECTION
# =====================================================

st.subheader("Country KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:

    nuclear_value = (
        latest_record["nuclear_electricity"]
        if "nuclear_electricity" in country_df.columns
        else 0
    )

    st.metric(
        "Nuclear Generation",
        f"{nuclear_value:,.2f}"
    )

with col2:

    renewable_value = (
        latest_record["renewables_electricity"]
        if "renewables_electricity" in country_df.columns
        else 0
    )

    st.metric(
        "Renewables",
        f"{renewable_value:,.2f}"
    )

with col3:

    emissions_value = (
        latest_record["co2_mtonne"]
        if "co2_mtonne" in country_df.columns
        else 0
    )

    st.metric(
        "CO₂ Emissions",
        f"{emissions_value:,.2f}"
    )

with col4:

    decarb_value = (
        latest_record["decarbonisation_score"]
        if "decarbonisation_score" in country_df.columns
        else 0
    )

    st.metric(
        "Decarbonisation",
        f"{decarb_value:,.2f}"
    )

st.divider()

# =====================================================
# GROWTH METRICS
# =====================================================

st.subheader("Growth Intelligence")

g1, g2 = st.columns(2)

with g1:

    nuclear_growth = country_nuclear_growth(
        df,
        selected_country
    )

    st.metric(
        "Nuclear Growth %",
        f"{nuclear_growth:.2f}%"
    )

with g2:

    renewable_growth_pct = renewable_growth(
        df,
        selected_country
    )

    st.metric(
        "Renewable Growth %",
        f"{renewable_growth_pct:.2f}%"
    )

st.divider()

# =====================================================
# ENERGY TRENDS
# =====================================================

st.subheader("Energy Production Trends")

trend_cols = []

for col in [
    "nuclear_electricity",
    "renewables_electricity"
]:
    if col in country_df.columns:
        trend_cols.append(col)

if len(trend_cols) > 0:

    fig = multi_line_chart(
        country_df,
        "year",
        trend_cols,
        f"{selected_country} Energy Trends"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# NUCLEAR TREND
# =====================================================

if "nuclear_electricity" in country_df.columns:

    st.subheader("⚛️ Nuclear Generation")

    fig = line_chart(
        country_df,
        "year",
        "nuclear_electricity",
        "Nuclear Electricity Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# RENEWABLE TREND
# =====================================================

if "renewables_electricity" in country_df.columns:

    st.subheader("🌱 Renewable Generation")

    fig = line_chart(
        country_df,
        "year",
        "renewables_electricity",
        "Renewable Electricity Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# EMISSIONS TREND
# =====================================================

if "co2_mtonne" in country_df.columns:

    st.subheader("📉 CO₂ Emissions Trend")

    fig = line_chart(
        country_df,
        "year",
        "co2_mtonne",
        "CO₂ Emissions"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# COUNTRY COMPARISON
# =====================================================

st.subheader("Country Comparison")

comparison_metric = st.selectbox(
    "Comparison Metric",
    [
        col
        for col in [
            "nuclear_electricity",
            "renewables_electricity",
            "co2_mtonne",
            "population",
            "gdp_per_capita_usd",
            "decarbonisation_score"
        ]
        if col in df.columns
    ]
)

fig = country_comparison_chart(
    df,
    comparison_countries,
    comparison_metric,
    f"{comparison_metric} Comparison"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# COUNTRY PROFILE
# =====================================================

st.subheader("Country Profile")

profile_cols = []

for col in [
    "country",
    "year",
    "population",
    "gdp_per_capita_usd",
    "co2_mtonne",
    "co2_per_capita_t",
    "nuclear_electricity",
    "renewables_electricity",
    "decarbonisation_score"
]:
    if col in country_df.columns:
        profile_cols.append(col)

st.dataframe(
    country_df[profile_cols].tail(10),
    use_container_width=True
)

st.divider()

# =====================================================
# ENERGY ECONOMICS
# =====================================================

if (
    "gdp_per_capita_usd" in country_df.columns
    and
    "decarbonisation_score" in country_df.columns
):

    st.subheader(
        "Economic vs Sustainability Analysis"
    )

    latest_df = (
        df.sort_values("year")
        .groupby("country")
        .tail(1)
    )

    fig = bubble_chart(
        latest_df,
        "gdp_per_capita_usd",
        "decarbonisation_score",
        "population",
        "nuclear_electricity"
        if "nuclear_electricity" in latest_df.columns
        else "population",
        "country",
        "GDP vs Sustainability"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# RAW DATA
# =====================================================

with st.expander("View Full Country Dataset"):

    st.dataframe(
        country_df,
        use_container_width=True
    )

# =====================================================
# DOWNLOAD
# =====================================================

csv = country_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Country Data",
    data=csv,
    file_name=f"{selected_country}_analysis.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    f"Country Intelligence Dashboard | {selected_country}"
)
