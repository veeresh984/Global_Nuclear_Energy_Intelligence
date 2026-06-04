import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data

from utils.analytics import (
    get_latest_data,
    top_decarbonisation_countries,
    average_decarbonisation_score,
    best_decarbonisation_country
)

from utils.charts import (
    decarbonisation_chart,
    histogram_chart,
    world_map
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Decarbonisation Intelligence",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

latest_df = get_latest_data(df)

# =====================================================
# HEADER
# =====================================================

st.title("📊 Decarbonisation Intelligence")

st.markdown("""
Evaluate sustainability performance,
energy transition readiness,
carbon reduction efforts,
and global decarbonisation leadership.
""")

st.divider()

# =====================================================
# VALIDATION
# =====================================================

if "decarbonisation_score" not in latest_df.columns:

    st.error(
        "Column 'decarbonisation_score' not found in dataset."
    )

    st.stop()

# =====================================================
# KPI SECTION
# =====================================================

avg_score = average_decarbonisation_score(df)

leader = best_decarbonisation_country(df)

max_score = latest_df[
    "decarbonisation_score"
].max()

countries = latest_df[
    "country"
].nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Score",
        f"{avg_score:.2f}"
    )

with col2:
    st.metric(
        "Top Country",
        leader
    )

with col3:
    st.metric(
        "Highest Score",
        f"{max_score:.2f}"
    )

with col4:
    st.metric(
        "Countries",
        countries
    )

st.divider()

# =====================================================
# TOP LEADERS
# =====================================================

st.subheader(
    "🏆 Global Decarbonisation Leaders"
)

leaders = top_decarbonisation_countries(
    df,
    top_n=15
)

fig = decarbonisation_chart(
    leaders,
    "Top Decarbonisation Countries"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# LEADERBOARD TABLE
# =====================================================

st.subheader(
    "📋 Sustainability Leaderboard"
)

cols = [
    c for c in [
        "country",
        "decarbonisation_score",
        "co2_mtonne",
        "co2_per_capita_t",
        "nuclear_electricity",
        "renewables_electricity"
    ]
    if c in leaders.columns
]

st.dataframe(
    leaders[cols],
    use_container_width=True
)

st.divider()

# =====================================================
# BOTTOM COUNTRIES
# =====================================================

st.subheader(
    "⚠️ Countries Requiring Attention"
)

bottom = (
    latest_df
    .sort_values(
        "decarbonisation_score",
        ascending=True
    )
    .head(15)
)

fig = px.bar(
    bottom,
    x="country",
    y="decarbonisation_score",
    color="decarbonisation_score",
    title="Lowest Decarbonisation Scores"
)

fig.update_layout(
    template="plotly_dark",
    xaxis_tickangle=-45,
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# SCORE DISTRIBUTION
# =====================================================

st.subheader(
    "📈 Score Distribution"
)

fig = histogram_chart(
    latest_df,
    "decarbonisation_score",
    "Distribution of Decarbonisation Scores"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# WORLD MAP
# =====================================================

if "iso_code" in latest_df.columns:

    st.subheader(
        "🌎 Global Sustainability Map"
    )

    fig = world_map(
        latest_df,
        "iso_code",
        "decarbonisation_score",
        "country",
        "Global Decarbonisation Scores"
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
):

    st.subheader(
        "📉 Carbon Intensity vs Sustainability"
    )

    fig = px.scatter(
        latest_df,
        x="co2_per_capita_t",
        y="decarbonisation_score",
        color="decarbonisation_score",
        size="population"
        if "population" in latest_df.columns
        else None,
        hover_name="country",
        title="Carbon Intensity vs Decarbonisation"
    )

    fig.update_layout(
        template="plotly_dark",
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# NUCLEAR CONTRIBUTION
# =====================================================

if (
    "nuclear_electricity" in latest_df.columns
):

    st.subheader(
        "⚛️ Nuclear Energy Contribution"
    )

    fig = px.scatter(
        latest_df,
        x="nuclear_electricity",
        y="decarbonisation_score",
        color="decarbonisation_score",
        hover_name="country",
        title="Nuclear Generation vs Decarbonisation"
    )

    fig.update_layout(
        template="plotly_dark",
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# RENEWABLE CONTRIBUTION
# =====================================================

if (
    "renewables_electricity" in latest_df.columns
):

    st.subheader(
        "🌱 Renewable Contribution"
    )

    fig = px.scatter(
        latest_df,
        x="renewables_electricity",
        y="decarbonisation_score",
        color="decarbonisation_score",
        hover_name="country",
        title="Renewables vs Decarbonisation"
    )

    fig.update_layout(
        template="plotly_dark",
        height=600
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
    "🤖 AI Sustainability Insights"
)

top_country = leaders.iloc[0]["country"]

top_score = leaders.iloc[0][
    "decarbonisation_score"
]

bottom_country = bottom.iloc[0]["country"]

bottom_score = bottom.iloc[0][
    "decarbonisation_score"
]

insights = [
    f"🏆 {top_country} currently leads global decarbonisation efforts with a score of {top_score:.2f}.",
    f"⚠️ {bottom_country} has the lowest decarbonisation score at {bottom_score:.2f}.",
    f"🌍 Average global decarbonisation score is {avg_score:.2f}.",
    f"📈 Countries with higher nuclear and renewable penetration generally achieve stronger sustainability performance."
]

for insight in insights:
    st.success(insight)

st.divider()

# =====================================================
# DOWNLOAD DATA
# =====================================================

csv = latest_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Decarbonisation Dataset",
    data=csv,
    file_name="decarbonisation_intelligence.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Global Nuclear Energy Intelligence Platform | Decarbonisation Intelligence"
)
