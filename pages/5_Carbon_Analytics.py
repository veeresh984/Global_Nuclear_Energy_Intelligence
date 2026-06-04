import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data

from utils.analytics import (
    get_latest_data,
    top_emission_countries,
    global_co2_emissions,
    average_carbon_intensity
)

from utils.charts import (
    top_country_chart,
    line_chart,
    world_map
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Carbon Analytics",
    page_icon="📉",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

latest_df = get_latest_data(df)

# =====================================================
# VALIDATION
# =====================================================

if "co2_mtonne" not in latest_df.columns:

    st.error(
        "Column 'co2_mtonne' not found in dataset."
    )

    st.stop()

# =====================================================
# HEADER
# =====================================================

st.title("📉 Carbon Emissions Intelligence")

st.markdown("""
Analyze carbon emissions,
carbon intensity,
per-capita emissions,
and sustainability risks across countries.
""")

st.divider()

# =====================================================
# KPIs
# =====================================================

global_co2 = global_co2_emissions(df)

highest_emitter = (
    latest_df.sort_values(
        "co2_mtonne",
        ascending=False
    )
    .iloc[0]
)

avg_intensity = 0

if "co2_per_capita_t" in latest_df.columns:
    avg_intensity = average_carbon_intensity(df)

countries = latest_df["country"].nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Global CO₂",
        f"{global_co2:,.0f}"
    )

with col2:
    st.metric(
        "Highest Emitter",
        highest_emitter["country"]
    )

with col3:
    st.metric(
        "Avg CO₂ / Capita",
        f"{avg_intensity:.2f}"
    )

with col4:
    st.metric(
        "Countries",
        countries
    )

st.divider()

# =====================================================
# GLOBAL TREND
# =====================================================

st.subheader(
    "🌍 Global CO₂ Trend"
)

co2_trend = (
    df.groupby("year")["co2_mtonne"]
    .sum()
    .reset_index()
)

fig = line_chart(
    co2_trend,
    "year",
    "co2_mtonne",
    "Global Carbon Emissions Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# TOP EMITTERS
# =====================================================

st.subheader(
    "🏭 Largest CO₂ Emitters"
)

top_emitters = top_emission_countries(
    df,
    20
)

fig = top_country_chart(
    top_emitters,
    "co2_mtonne",
    "Top Carbon Emitters"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(
    top_emitters[
        [
            col for col in [
                "country",
                "co2_mtonne",
                "co2_per_capita_t",
                "population"
            ]
            if col in top_emitters.columns
        ]
    ],
    use_container_width=True
)

st.divider()

# =====================================================
# PER CAPITA ANALYSIS
# =====================================================

if "co2_per_capita_t" in latest_df.columns:

    st.subheader(
        "👤 CO₂ Per Capita Analysis"
    )

    top_per_capita = (
        latest_df
        .sort_values(
            "co2_per_capita_t",
            ascending=False
        )
        .head(20)
    )

    fig = px.bar(
        top_per_capita,
        x="country",
        y="co2_per_capita_t",
        color="co2_per_capita_t",
        title="Highest CO₂ Per Capita"
    )

    fig.update_layout(
        template="plotly_dark",
        height=600,
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# CARBON INTENSITY ANALYSIS
# =====================================================

if (
    "co2_per_capita_t" in latest_df.columns
    and
    "decarbonisation_score" in latest_df.columns
):

    st.subheader(
        "📊 Carbon Intensity vs Sustainability"
    )

    fig = px.scatter(
        latest_df,
        x="co2_per_capita_t",
        y="decarbonisation_score",
        color="decarbonisation_score",
        hover_name="country",
        size="population"
        if "population" in latest_df.columns
        else None,
        title="Carbon Intensity vs Decarbonisation"
    )

    fig.update_layout(
        template="plotly_dark",
        height=700
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# GDP VS EMISSIONS
# =====================================================

if (
    "gdp_per_capita_usd" in latest_df.columns
):

    st.subheader(
        "💰 GDP vs Carbon Emissions"
    )

    fig = px.scatter(
        latest_df,
        x="gdp_per_capita_usd",
        y="co2_mtonne",
        color="co2_mtonne",
        hover_name="country",
        size="population"
        if "population" in latest_df.columns
        else None,
        title="GDP vs Carbon Emissions"
    )

    fig.update_layout(
        template="plotly_dark",
        height=700
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# NUCLEAR IMPACT
# =====================================================

if (
    "nuclear_electricity" in latest_df.columns
):

    st.subheader(
        "⚛️ Nuclear Energy Impact"
    )

    fig = px.scatter(
        latest_df,
        x="nuclear_electricity",
        y="co2_mtonne",
        color="co2_mtonne",
        hover_name="country",
        title="Nuclear Generation vs CO₂"
    )

    fig.update_layout(
        template="plotly_dark",
        height=700
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# GLOBAL MAP
# =====================================================

if "iso_code" in latest_df.columns:

    st.subheader(
        "🌎 Global Carbon Emissions Map"
    )

    fig = world_map(
        latest_df,
        "iso_code",
        "co2_mtonne",
        "country",
        "Global Carbon Emissions"
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
    "📈 Carbon Correlation Matrix"
)

corr_cols = [
    col for col in [
        "co2_mtonne",
        "co2_per_capita_t",
        "nuclear_electricity",
        "renewables_electricity",
        "population",
        "gdp_per_capita_usd",
        "decarbonisation_score"
    ]
    if col in latest_df.columns
]

corr = latest_df[
    corr_cols
].corr()

fig = px.imshow(
    corr,
    text_auto=".2f",
    aspect="auto",
    title="Correlation Matrix"
)

fig.update_layout(
    template="plotly_dark",
    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# AI INSIGHTS
# =====================================================

st.subheader(
    "🤖 Carbon Intelligence Insights"
)

top_country = highest_emitter["country"]

top_value = highest_emitter[
    "co2_mtonne"
]

insights = [

    f"⚠️ {top_country} is currently the largest CO₂ emitter with {top_value:,.2f} million tonnes.",

    f"🌍 Total global emissions currently stand at {global_co2:,.2f} million tonnes.",

    "📈 Higher decarbonisation scores are generally associated with lower carbon intensity.",

    "⚛️ Countries with strong nuclear energy adoption often demonstrate lower carbon intensity compared to fossil-heavy economies.",

    "🌱 Renewable energy growth continues to be a major contributor to long-term emissions reduction."
]

for insight in insights:

    st.success(insight)

st.divider()

# =====================================================
# DOWNLOAD
# =====================================================

csv = latest_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Carbon Dataset",
    data=csv,
    file_name="carbon_analytics.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Global Nuclear Energy Intelligence Platform | Carbon Analytics"
)
