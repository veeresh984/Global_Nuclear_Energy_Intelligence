import streamlit as st
import pandas as pd

from utils.data_loader import (
    load_data
)

from utils.analytics import (
    executive_scorecard,
    get_latest_data,
    top_nuclear_countries,
    top_renewable_countries,
    top_emission_countries,
    correlation_matrix
)

from utils.charts import (
    line_chart,
    multi_line_chart,
    top_country_chart,
    correlation_heatmap,
    world_map
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Global Overview",
    page_icon="🌍",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

latest_df = get_latest_data(df)

scorecard = executive_scorecard(df)

# =====================================================
# HEADER
# =====================================================

st.title("🌍 Global Energy Intelligence Overview")

st.markdown(
    """
    Analyze worldwide nuclear energy production,
    renewable energy growth,
    carbon emissions,
    and sustainability performance.
    """
)

st.divider()

# =====================================================
# KPI SECTION
# =====================================================

st.subheader("Executive KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Countries",
        f"{scorecard['countries']:,}"
    )

with col2:
    st.metric(
        "Latest Year",
        scorecard["latest_year"]
    )

with col3:
    st.metric(
        "Nuclear Generation",
        f"{scorecard['nuclear_generation']:,.0f}"
    )

with col4:
    st.metric(
        "CO₂ Emissions",
        f"{scorecard['co2_emissions']:,.0f}"
    )

st.divider()

# =====================================================
# GLOBAL TRENDS
# =====================================================

st.subheader("Global Energy Trends")

agg_cols = []

possible_cols = [
    "nuclear_electricity",
    "renewables_electricity",
    "co2_mtonne"
]

for col in possible_cols:

    if col in df.columns:
        agg_cols.append(col)

global_trend = (
    df.groupby("year")[agg_cols]
    .sum()
    .reset_index()
)

if len(agg_cols) > 1:

    fig = multi_line_chart(
        global_trend,
        "year",
        agg_cols,
        "Global Energy Trends"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# NUCLEAR TREND
# =====================================================

if "nuclear_electricity" in global_trend.columns:

    st.subheader(
        "⚛️ Global Nuclear Generation Trend"
    )

    fig = line_chart(
        global_trend,
        "year",
        "nuclear_electricity",
        "Nuclear Electricity Generation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# RENEWABLE TREND
# =====================================================

if "renewables_electricity" in global_trend.columns:

    st.subheader(
        "🌱 Renewable Energy Growth"
    )

    fig = line_chart(
        global_trend,
        "year",
        "renewables_electricity",
        "Renewable Electricity Generation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# CO2 TREND
# =====================================================

if "co2_mtonne" in global_trend.columns:

    st.subheader(
        "📉 Global CO₂ Emissions"
    )

    fig = line_chart(
        global_trend,
        "year",
        "co2_mtonne",
        "Global CO₂ Emissions Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# TOP COUNTRIES
# =====================================================

left, right = st.columns(2)

with left:

    st.subheader(
        "🏆 Top Nuclear Nations"
    )

    top_nuclear = top_nuclear_countries(
        df,
        top_n=10
    )

    if not top_nuclear.empty:

        fig = top_country_chart(
            top_nuclear,
            "nuclear_electricity",
            "Top Nuclear Producers"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

with right:

    st.subheader(
        "🌱 Top Renewable Nations"
    )

    top_renewables = top_renewable_countries(
        df,
        top_n=10
    )

    if not top_renewables.empty:

        fig = top_country_chart(
            top_renewables,
            "renewables_electricity",
            "Top Renewable Producers"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.divider()

# =====================================================
# TOP EMITTERS
# =====================================================

if "co2_mtonne" in latest_df.columns:

    st.subheader(
        "⚠️ Largest CO₂ Emitters"
    )

    top_emitters = top_emission_countries(
        df,
        top_n=15
    )

    fig = top_country_chart(
        top_emitters,
        "co2_mtonne",
        "Largest CO₂ Emitters"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# WORLD MAP
# =====================================================

if (
    "iso_code" in latest_df.columns
    and
    "nuclear_electricity" in latest_df.columns
):

    st.subheader(
        "🗺️ Global Nuclear Energy Map"
    )

    fig = world_map(
        latest_df,
        "iso_code",
        "nuclear_electricity",
        "country",
        "Global Nuclear Generation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# CORRELATION ANALYSIS
# =====================================================

st.subheader(
    "📊 Correlation Analysis"
)

corr = correlation_matrix(df)

fig = correlation_heatmap(corr)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# DATA SNAPSHOT
# =====================================================

st.subheader("Dataset Snapshot")

st.dataframe(
    latest_df.head(20),
    use_container_width=True
)

# =====================================================
# DOWNLOAD SECTION
# =====================================================

csv = latest_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Latest Year Data",
    data=csv,
    file_name="latest_energy_data.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Global Nuclear Energy Intelligence Dashboard | Global Overview"
)
